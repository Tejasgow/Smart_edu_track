from django.shortcuts import render
from rest_framework .views import APIView
from rest_framework .response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import markentrySerializer
from .models import Mark,Exam
from .serializers import examSerializer
from rest_framework.generics import ListCreateAPIView
from ACCOUNTS.permissions import IsTeacherOrPrincipal
from rest_framework import generics

class MarkEntryListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsTeacherOrPrincipal]

    def get(self, request):
        """
        List all marks
        """
        marks = Mark.objects.all()
        serializer = markentrySerializer(marks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Accepts a list of mark entries for students.
        """
        serializer = markentrySerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save(entered_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

class ExamListCreateView(ListCreateAPIView):
    queryset = Exam.objects.all().order_by('-date')
    serializer_class = examSerializer
    permission_classes = [IsAuthenticated, IsTeacherOrPrincipal]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
