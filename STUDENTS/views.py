from django.shortcuts import render
from rest_framework import generics,permissions
from .serializers import StudentRegistrationSerializer , LinkParentSerializer,SectionSerializer,StandardSerializer
from .models import Student , ParentStudent , Standard , Section


class IsTeacher(permissions.BasePermission):
    def has_permission(self,request,view):
        return request.user.is_authenticated and request.user.role in ["teacher"]
    

class StudentRegistrationView(generics.CreateAPIView):
    queryset= Student.objects.all()
    serializer_class = StudentRegistrationSerializer
    permission_classes = [IsTeacher]

class LinkparentToStudentView(generics.CreateAPIView):
    queryset = ParentStudent.objects.all()
    serializer_class = LinkParentSerializer
    permission_classes = [IsTeacher]


class StandardListCreatView(generics.ListCreateAPIView):
    queryset = Standard.objects.all()
    serializer_class = StandardSerializer
    permission_classes = [IsTeacher]

class SectionListCreateView(generics.ListCreateAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [IsTeacher]