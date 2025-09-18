from django.shortcuts import render
from .models import User, Classroom
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
# Create your views here.
class CreateTeacherView(CreateAPIView):
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
class CreateStudentView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def post(self, request, *args, **kwargs):
        
        if request.user.role != 'teacher':
            return Response(
                {"error": "Only teachers can add students"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().post(request, *args, **kwargs)