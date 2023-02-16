from datetime import datetime

from django.http import Http404
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
    ScanDataSerializer, UserConnectionSerializer
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
        return Response({'msg': 'Password Changed Successfully'}, status=status.HTTP_200_OK)


class SendPasswordResetEmailView(CreateAPIView):
    renderer_classes = [UserRenderer]
    serializer_class = SendPasswordResetEmailSerializer
    allowed_methods = ('POST',)
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None, **kwargs):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)


class UserPasswordResetView(CreateAPIView):
    renderer_classes = [UserRenderer]
    serializer_class = UserPasswordResetSerializer
    allowed_methods = ('POST',)
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid': uid, 'token': token})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Reset Successfully'}, status=status.HTTP_200_OK)


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
    # permission_classes = [IsAuthenticated]
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
            user_conn = self.get_object()
        except Http404:
            return Response({"error": "UserConnection not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserConnectionSerializer(user_conn, data=request.data, partial=True)
        if serializer.is_valid():
            if "is_connection_alive" in request.data:
                if request.data.get("is_connection_alive") == "yes":
                    serializer.validated_data["status_active"] = True
                    serializer.validated_data["last_status"] = timezone.now()
                else:
                    serializer.validated_data["status_active"] = False
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self):
        user_id = self.request.user.id
        user_conn = UserConnection.objects.get(id=user_id)
        return user_conn


# class UserConnectionView(CreateAPIView):
#     # permission_classes = [IsAuthenticated]
#     renderer_classes = [UserRenderer]
#     serializer_class = UserConnectionSerializer
#     allowed_methods = ('POST', 'PUT')
#     parser_classes = [MultiPartParser, FormParser]
#
#     def post(self, request, format=None, **kwargs):
#         serializer = UserConnectionSerializer(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         return Response({'msg': 'User Connection Established Successfully'}, status=status.HTTP_201_CREATED)
#
#     def put(self, request, *args, **kwargs):
#         try:
#             user_conn = self.get_object()
#         except Http404:
#             return Response({"error": "UserConnection not found"}, status=status.HTTP_404_NOT_FOUND)
#
#         serializer = UserConnectionSerializer(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({'msg': 'User Connection Updated Successfully'}, status=status.HTTP_200_OK)
#
#     def get_object(self):
#         user_id = self.request.user.id
#         user_conn = UserConnection.objects.get(id=user_id)
#         return user_conn


class ScanDataView(CreateAPIView):
    # permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]
    serializer_class = ScanDataSerializer
    allowed_methods = ('POST',)
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None, **kwargs):
        serializer = ScanDataSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Data Scanned Successfully'}, status=status.HTTP_201_CREATED)
