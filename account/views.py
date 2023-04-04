import asyncio
import json
import os
import time

import requests
import websockets
from datetime import datetime

from asgiref.sync import async_to_sync
from datetime import datetime, timedelta
from channels.layers import get_channel_layer
from django.http import Http404, JsonResponse
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from account.models import User, UserConnection, Scan, ScanData
from rest_framework.views import APIView
from machine_learning import *

from account.models import ScanData
from django.views.decorators.http import require_http_methods
from account.serializers import SendPasswordResetEmailSerializer, UserChangePasswordSerializer, UserLoginSerializer, \
    UserPasswordResetSerializer, UserProfileSerializer, UserRegistrationSerializer, UpdateRegisterUserSerializer, \
    UserConnectionSerializer, IsScanSerializer, ScanDataSerializer, SysInfoSerializer, ItgnirSerializer, \
    PredictSerializer, ModelTrainingSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.permissions import IsAuthenticated


# Generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(CreateAPIView):
    renderer_classes = [UserRenderer]
    serializer_class = UserRegistrationSerializer
    allowed_methods = ('POST',)
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'token': token, 'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)


class UserLoginView(CreateAPIView):
    renderer_classes = [UserRenderer]
    serializer_class = UserLoginSerializer
    allowed_methods = ('POST',)
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg': 'Login Success'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors': {'non_field_errors': ['Email or Password is not Valid']}},
                            status=status.HTTP_404_NOT_FOUND)


class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChangePasswordView(CreateAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    serializer_class = UserChangePasswordSerializer
    allowed_methods = ('POST',)
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None, **kwargs):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Changed Successfully'}, status=status.HTTP_201_CREATED)


class SendPasswordResetEmailView(CreateAPIView):
    renderer_classes = [UserRenderer]
    serializer_class = SendPasswordResetEmailSerializer
    allowed_methods = ('POST',)
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None, **kwargs):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Reset link send. Please check your Email'}, status=status.HTTP_201_CREATED)


class UserPasswordResetView(CreateAPIView):
    renderer_classes = [UserRenderer]
    serializer_class = UserPasswordResetSerializer
    allowed_methods = ('POST',)
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid': uid, 'token': token})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Reset Successfully'}, status=status.HTTP_201_CREATED)


class UpdateRegisterUserView(CreateAPIView):
    renderer_classes = [UserRenderer]
    serializer_class = UpdateRegisterUserSerializer
    allowed_methods = ('PUT',)
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request, format=None):
        serializer = UpdateRegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'User type update successfully'}, status=status.HTTP_200_OK)


def lobby(request):
    return render(request, 'account/lobby.html')


class UserConnectionView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]
    serializer_class = UserConnectionSerializer
    allowed_methods = ('POST', 'PUT')
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None, **kwargs):
        serializer = UserConnectionSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'User Connection Established Successfully'}, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        try:
            machine_name = request.data['machine_name']
            user_id = request.data['user_id']
            user_conn = self.get_object(machine_name, user_id)
        except Http404:
            return Response({"error": "UserConnection not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserConnectionSerializer(user_conn, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'User Connection Updated Successfully'}, status=status.HTTP_200_OK)

    def get_object(self, machine_name, user_id):
        user_conn = UserConnection.objects.get(machine_name=machine_name, user_id=user_id)
        return user_conn


async def send_and_receive(request_data):
    try:
        user_id = request_data['user_id']
        from .consumers import connections
        await connections[user_id].receive(json.dumps(request_data))
    except Exception as e:
        return print({f'Error: {e}'})


class IsScanView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]
    serializer_class = IsScanSerializer
    allowed_methods = ('POST',)
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None, **kwargs):
        try:
            if len(request.data) == 0:
                return Response({f'Error': 'invalid payload'}, status=status.HTTP_400_BAD_REQUEST)
            is_scan = dict(request.data)['is_scan'][0]
            if is_scan == 'yes':
                scan_instance = Scan.objects.create()
                user_id = request.user.id
                scan_id = str(scan_instance.scan_id)
                async_to_sync(send_and_receive)(
                    request_data={'is_scan_data': 'yes', 'user_id': user_id, 'scan_id': scan_id})
                return Response({'message': 'data Scanning is in progress'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'Error': 'select is_scan yes for scanning the data'},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({f'Error: {e}'}, status=status.HTTP_400_BAD_REQUEST)


class ScanDataView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]
    serializer_class = ScanDataSerializer
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None, **kwargs):
        machine_name = request.data['machine_name']
        user_id = request.data['user_id']
        scan_id = request.data['scan_id']
        new_scan_id = scan_id.replace("-", "").replace("_", "")
        user_connection_obj = UserConnection.objects.get(machine_name=machine_name, user_id=user_id)
        scan_obj = Scan.objects.get(scan_id=scan_id)
        energy_wavelength_data = request.data.getlist('energy_wavelength_data')
        scan_data_list = []
        for data in energy_wavelength_data:
            energy, wavelength = eval(data)
            scan_data_list.append(
                ScanData(
                    user_connection=user_connection_obj,
                    scan_connection=scan_obj,
                    energy=energy,
                    wavelength=wavelength
                )
            )
        ScanData.objects.bulk_create(scan_data_list)

        try:
            # create instance of DataProcessor class
            data_processor = DataProcessor(username='root', password='U$er123',
                                           host='localhost', database='qtdb')

            # connect to database and retrieve data
            cnx, cursor = data_processor.connect_to_database()
            db_rows = data_processor.retrieve_data_for_prediction(cursor, new_scan_id)

            # preprocess data
            latest_sample = data_processor.sample_data(db_rows)

            # close database connection
            cnx.close()

            # create instance of ModelTrainer class
            model_trainer = ModelTrainer(X_train_scaled=None, y_train=None)

            # load the pre-trained model
            loaded_grid = model_trainer.load_model()

            # make predictions
            pred = loaded_grid.predict(latest_sample)[0]

            print('Successfully getting the prediction')

            scan_instance = Scan.objects.get(scan_id=scan_id)
            scan_instance.predict_value = pred
            scan_instance.save()

            print('Data Scanned Successfully')
            return Response({'msg': 'Data Scanned Successfully'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({f'Error: {e}'}, status=status.HTTP_400_BAD_REQUEST)


class SysInfoView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]
    serializer_class = SysInfoSerializer

    def get(self, request, format=None):
        try:
            user_id = request.user.id
            userconnection_objects = UserConnection.objects.filter(user_id=user_id)
            connected_user_list = []
            for obj in userconnection_objects:
                data = {
                    'machine_name': obj.machine_name,
                    'mac_address': obj.mac_address
                }
                connected_user_list.append(data)
            message = {
                'message': 'machine names and mac addresses for login user',
                'connected_user_info': connected_user_list
            }
            return Response(message, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({f'Error: {e}'}, status=status.HTTP_400_BAD_REQUEST)


class ItgnirDataView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]
    serializer_class = ItgnirSerializer

    def post(self, request, format=None):
        try:
            if len(request.data) == 0:
                return Response({f'Error': 'invalid payload'}, status=status.HTTP_400_BAD_REQUEST)
            machine_name = request.data['machine_name']
            userconnection_obj = UserConnection.objects.get(machine_name=machine_name)
            userconnection_id = userconnection_obj.id
            current_time = timezone.now()
            time_10_mints_ago = current_time - timezone.timedelta(minutes=10)
            scan_objects_list = ScanData.objects.filter(
                user_connection_id=userconnection_id,
                created_at__gte=time_10_mints_ago
            )
            itgnir_data = []
            for obj in scan_objects_list:
                energy = obj.energy
                wavelength = obj.wavelength
                data = {
                    'energy': energy,
                    'wavelength': wavelength
                }
                itgnir_data.append(data)
            message = {
                'message': 'energy and wavelength data between the last 2 days',
                'itgnir_data': itgnir_data
            }
            return Response(message, status=status.HTTP_200_OK)
        except Exception as e:

            return Response({f'Error: {e}'}, status=status.HTTP_400_BAD_REQUEST)


class PredictView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]
    serializer_class = PredictSerializer

    def post(self, request, format=None):
        try:
            scan_id = request.data['scan_id']
            scan_instance = Scan.objects.get(scan_id=scan_id)
            predict_value = scan_instance.predict_value
            if not predict_value:
                message = {
                    'message': 'Prediction is in progress',
                }
                return Response(message, status=status.HTTP_200_OK)
            message = {
                'message': 'Prediction completed successfully',
                'predict_value': predict_value
            }
            return Response(message, status=status.HTTP_201_CREATED)
        except Exception as e:
            error_message = f'{",".join(e)}'
            return Response({'Error': error_message}, status=status.HTTP_400_BAD_REQUEST)


class ModelTrainingView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]
    serializer_class = ModelTrainingSerializer

    def get(self, request, format=None):
        try:
            # create instance of DataProcessor class
            data_processor = DataProcessor(username='root', password='U$er123',
                                           host='localhost', database='qtdb')

            # connect to database and retrieve data
            cnx, cursor = data_processor.connect_to_database()
            db_rows = data_processor.retrieve_data(cursor)

            # preprocess data
            X_train_scaled, y_train, X_test_scaled, = data_processor.preprocess_data(db_rows)

            # close database connection
            cnx.close()

            # create instance of ModelTrainer class
            model_trainer = ModelTrainer(X_train_scaled=X_train_scaled, y_train=y_train)

            # train the model
            grid, train_score = model_trainer.train_model()

            # save the model
            model_trainer.save_model(grid)

            # load the model
            model_trainer.load_model()

            # format predictions as a JSON response
            response_data = {
                'message': 'Successfully trained the SVR model and saved it as gs_object.pkl file'
            }
            return JsonResponse(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            error_message = str(e)
            return Response({'Error': error_message}, status=status.HTTP_400_BAD_REQUEST)
