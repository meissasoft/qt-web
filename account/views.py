import asyncio
import json
import time

import websockets
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import Http404, JsonResponse
from django.utils import timezone
from rest_framework.generics import CreateAPIView
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from account.models import User, UserConnection
from rest_framework.views import APIView

from account.models import ScanData
from account.serializers import SendPasswordResetEmailSerializer, UserChangePasswordSerializer, UserLoginSerializer, \
    UserPasswordResetSerializer, UserProfileSerializer, UserRegistrationSerializer, UpdateRegisterUserSerializer, \
    ScanDataSerializer, UserConnectionSerializer, IsScanSerializer
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
            user_conn = self.get_object(machine_name)
        except Http404:
            return Response({"error": "UserConnection not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserConnectionSerializer(user_conn, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'User Connection Updated Successfully'}, status=status.HTTP_200_OK)

    def get_object(self, machine_name):
        user_conn = UserConnection.objects.get(machine_name=machine_name)
        return user_conn


async def send_and_receive(request_data):
    try:
        user_id = request_data['user_id']
        from .consumers import connections
        await connections[user_id].receive(json.dumps(request_data))
    except Exception as e:
        return Response({f'Error: {e}'}, status=status.HTTP_400_BAD_REQUEST)


class IsScanView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]
    serializer_class = IsScanSerializer
    allowed_methods = ('POST',)
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None, **kwargs):
        is_scan = dict(request.data)['is_scan'][0]
        if is_scan == 'yes':
            user_id = request.user.id
            async_to_sync(send_and_receive)(request_data={'is_scan_data': 'yes', 'user_id': user_id})
            return Response({'msg': 'ok'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'Error': 'Select is_scan yes for scanning the data'}, status=status.HTTP_400_BAD_REQUEST)


class ScanDataView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]
    allowed_methods = ('POST',)
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None, **kwargs):
        machine_name = request.data['machine_name']
        user_connection_obj = UserConnection.objects.get(machine_name=machine_name)
        request_data = {'connection_user': user_connection_obj}
        energy_wavelength_data = request.data.getlist('energy_wavelength_data')
        energy_wavelength_list = [eval(data) for data in energy_wavelength_data]
        for energy, wavelength in energy_wavelength_list:
            request_data['energy'] = energy
            request_data['wavelength'] = wavelength
            ScanData.objects.create(**request_data)
        print('Data Scanned Successfully')
        return Response({'msg': 'Data Scanned Successfully'}, status=status.HTTP_201_CREATED)
