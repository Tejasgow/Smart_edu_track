from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import (
    StudentRegistrationSerializer, LinkParentSerializer,
    SectionSerializer, StandardSerializer,
    AttendanceMarkSerializer, AttendanceSerializer,
    SubjectSerializer
)
from .models import Student, ParentStudent, Standard, Section, Attendance ,Subject
from ACCOUNTS.models import user
import json



class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["teacher"]

class StudentRegistrationView(generics.CreateAPIView):
    queryset = Student.objects.all()
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

class SubjectListCreateView(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsTeacher]

class AttendanceMarkView(generics.CreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceMarkSerializer
    permission_classes = []  # Add your permission classes here as needed

    def post(self, request, *args, **kwargs):
        data = request.data
        many = isinstance(data, list)
        serializer = self.get_serializer(data=data, many=many)
        serializer.is_valid(raise_exception=True)

        teacher = request.user if request.user.is_authenticated else User.objects.get(id=10)
        records = []

        validated_items = serializer.validated_data if many else [serializer.validated_data]

        for item in validated_items:
            attendance, created = Attendance.objects.update_or_create(
                student_id=item["student_id"],
                date=item["date"],
                defaults={
                    "status": item["status"],
                    "marked_by": teacher
                }
            )
            records.append(attendance)

        return Response(
            AttendanceSerializer(records, many=True).data,
            status=status.HTTP_200_OK
        )
class StudentAttendanceView(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        student_id = self.kwargs["student_id"]
        if self.request.user.role == "student" and self.request.user.id != int(student_id):
            return Attendance.objects.none()
        return Attendance.objects.filter(student_id=student_id).order_by("-date")

class ClassAttendanceView(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsTeacher, IsAuthenticated]

    def get_queryset(self):
        section_id = self.kwargs["section_id"]
        section = Section.objects.get(id=section_id)
        date = self.request.query_params.get("date")
        user_ids = [student.user.id for student in Student.objects.filter(section=section)]
        students = user.objects.filter(id__in=user_ids, role="student")

        if date:
            return Attendance.objects.filter(student__in=students, date=date)
        return Attendance.objects.filter(student__in=students).order_by("-date")

# Utility
def calculate_attendance_percentage(present_days, total_days):
    if total_days == 0:
        return "0%"
    percentage = (present_days / total_days) * 100
    return f"{percentage:.2f}%"

class AttendanceReportPrincipalView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = Attendance.objects.all()
        standard = request.query_params.get("standard")
        section = request.query_params.get("section")
        from_date = request.query_params.get("from_date")
        to_date = request.query_params.get("to_date")

        if standard:
            std = Standard.objects.filter(name=standard)
            students = Student.objects.filter(standard=std)
            users = [student.user for student in students]
            queryset = queryset.filter(student__in=users)
        if section:
            sec = Section.objects.filter(name=section)
            students = Student.objects.filter(section=sec)
            users = [student.user for student in students]
            queryset = queryset.filter(student__in=users)
        if from_date and to_date:
            queryset = queryset.filter(date__range=[from_date, to_date])
        
        summary_data = []
        student_ids = queryset.values_list("student_id", flat=True).distinct()

        for sid in student_ids:
            student_record = queryset.filter(student_id=sid)
            if not student_record.exists():
                continue
            user = student_record.first().student
            total_days = student_record.count()
            total_present = student_record.filter(status="PRESENT").count()
            total_absent = student_record.filter(status="ABSENT").count()
            student = Student.objects.filter(user=user)
            summary_data.append({
                "student_name": f"{user.first_name} {user.last_name}",
                "standard": student.first().standard.name if student.exists() else "",
                "section": student.first().section.name if student.exists() else "",
                "total_present": total_present,
                "total_absent": total_absent,
                "attendance_percentage": calculate_attendance_percentage(total_present, total_days)
            })

        total_students = len(student_ids)
        total_days = queryset.values("date").distinct().count()
        overall_present = queryset.filter(status="PRESENT").count()
        overall_percentage = calculate_attendance_percentage(overall_present, queryset.count())

        return Response({
            "summary": {
                "total_students": total_students,
                "total_days": total_days,
                "average_attendance": overall_percentage
            },
            "records": summary_data
        })

class AttendanceReportParentView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        parent = request.user
        linked_students = [link.student for link in ParentStudent.objects.filter(parent=parent)]
        from_date = request.query_params.get("from_date")
        to_date = request.query_params.get("to_date")

        data = []
        
        for student_ in linked_students:
            user = student_.user
            user_records = Attendance.objects.filter(student=user)
            if from_date and to_date:
                user_records = user_records.filter(date__range=[from_date, to_date])

            if not user_records.exists():
                continue
        
            total_days = user_records.count()
            total_present = user_records.filter(status="PRESENT").count()
            total_absent = user_records.filter(status="ABSENT").count()

            child_data = {
                "student_name": f"{student_.users.first_name} {student_.users.last_name}",
                "standard": student_.standard.name,
                "section": student_.section.name,
                "summary": {
                    "total_days": total_days,
                    "present": total_present,
                    "absent": total_absent,
                    "percentage": calculate_attendance_percentage(total_present, total_days)
                },
               "records": AttendanceMarkSerializer(user_records, many=True).data

            }

            data.append(child_data)

        return Response({"children": data})
