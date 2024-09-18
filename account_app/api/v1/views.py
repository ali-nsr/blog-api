from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .serializers import (
    RegisterSerializer, ChangePasswordSerializer, CustomTokenObtainPairSerializer, ProfileSerializer,
    ResendVerificationSerializer
)
from account_app.models import Profile
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from account_app.utils import SendEmailThread
import jwt
from django.conf import settings

User = get_user_model()


class RegisterApiView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            user_email = serializer.validated_data['email']
            data = {
                'email': serializer.validated_data['email'],
                'phone': serializer.validated_data['phone'],
                'welcome': 'welcome :)',
            }
            # sending verification code via email or sms.
            user = get_object_or_404(User, email=user_email)
            token = self.get_tokens_for_user(user)

            # use threading for better performance. celery does the job too
            SendEmailThread(
                'subject', f'http://127.0.0.1:8000/account/api/v1/verification/confirm/{token}/', 'admin@admin.com',
                [user_email]
            ).start()
            # end sending verification code
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


# class CustomObtainAuthToken(ObtainAuthToken):
#     serializer_class = CustomAuthTokenSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data,
#                                            context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({
#             'token': token.key,
#             'user_id': user.pk,
#             'email': user.email
#         })


# class CustomDeleteAuthToken(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request, *args, **kwargs):
#         request.user.auth_token.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ChangePasswordApiView(generics.GenericAPIView):
    model = User
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    # def get_object(self):
    #     return self.request.user

    def put(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not user.check_password(serializer.data['old_password']):
                return Response({'old_password': 'wrong password'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data['new_password'])
            user.save()
            return Response({'detail': 'password changed successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileApiView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer

    def get_object(self):
        obj = get_object_or_404(Profile, user=self.request.user)
        return obj


class VerificationTokenApiView(APIView):
    def get(self, request, token, *args, **kwargs):
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            print(token)
            user_id = token.get('user_id')
            print(user_id)
            user = User.objects.get(id=user_id)
            if user.is_verified:
                return Response({'details': 'your account is already verified'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                print('ok')
                user.is_verified = True
                user.save()
            return Response({'details': 'user verified successfully'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidSignatureError:
            return Response(status=status.HTTP_400_BAD_REQUEST)



class ResendVerificationTokenApiView(generics.GenericAPIView):
    serializer_class = ResendVerificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = ResendVerificationSerializer(data=request.data)
        if serializer.is_valid():

            user = serializer.validated_data['user']
            token = self.get_tokens_for_user(user)
            # use threading for better performance. celery does the job too
            SendEmailThread(
                'subject', f'http://127.0.0.1:8000/account/api/v1/verification/confirm/{token}/', 'admin@admin.com',
                [user.email]
            ).start()
            # end sending verification code
            return Response({'details': 'verification email send again'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
