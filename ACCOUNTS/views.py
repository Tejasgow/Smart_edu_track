from django.shortcuts import render
from rest_framework.generics import CreateAPIView 
from .serializers import CreateUserserializer , sessionloginserializer  , PasswordResetRequestSerializer , PasswordResetConfirmSerializer
from .models import user
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.views import status
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth import login,logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes


class createTeacherParentView(CreateAPIView):
    serializer_class=CreateUserserializer
    permission_classes=[IsAuthenticated]
    authentication_classes=[SessionAuthentication]


    def post(self,request,*args,**kwargs):
        return super().post(request,*args,**kwargs)


class sessionloginview(APIView):
    def post(self,request,*args,**kwargs):
        serializer = sessionloginserializer(data=request.data)
        if serializer.is_valid():
            users = serializer.validated_data
            login(request,user)
            return Response({
                "message":"login successfully",
                "users":{
                    "id":users.id,
                    "username":users.username,
                    "email":users.email,
                    "role":users.role,
                }
            },status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_401_UNAUTHORIZED)
    

class sessionlogoutview(APIView):
    def get(self,request,*args,**kwargs):
        logout(request)
        return Response({"message":"logout successfull"},status=status.HTTP_200_OK)



class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        users = user.objects.get(email=serializer.validated_data['email'])
        uid = urlsafe_base64_decode(force_bytes(users.pk))
        token = default_token_generator.make_token(users)

        reset_link = f"http://example.com/reset-password-confirm/?uid={uid}&token={token}"

        return Response(
            {"message": "Password reset link has been sent to your email.", "reset_link": reset_link}, 
            status=status.HTTP_200_OK
            )
    

class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            {"message": "Password reset successful"},
            status=status.HTTP_200_OK
            )