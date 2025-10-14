from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import MarkEntrySerializer
from .models import Mark,Exam
from .serializers import ExamSerializer
from rest_framework.generics import ListCreateAPIView
from ACCOUNTS.permissions import IsTeacherOrPrincipal


# Create your views here.

class MarkEntryView(APIView):
    permission_classes = [IsAuthenticated, IsTeacherOrPrincipal]

    def post(self, request):
        """
        Accepts a list of marks entries for students.
        Example payload:
        [
            {
                "exam": 1,
                "student": 3,
                "subject": 2,
                "marks_obtained": 45,
                "max_marks": 50,
                "remarks": "Good improvement"
            },
            ...
        ]
        """
        serializer = MarkEntrySerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save(entered_by=request.user)
            return Response({"message": "Marks saved successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExamListCreateView(ListCreateAPIView):
    queryset = Exam.objects.all().order_by('-date')
    serializer_class = ExamSerializer
    permission_classes = [IsAuthenticated, IsTeacherOrPrincipal]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
