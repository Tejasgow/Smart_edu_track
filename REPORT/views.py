from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from ACCOUNTS.permissions import IsTeacherOrPrincipal,IsPrincipal
from STUDENTS.models import Student
from PERFORMANCE.models import Mark
from django.db.models import Avg


class ReportCardView(APIView):
    permission_classes = [IsAuthenticated, IsTeacherOrPrincipal, IsPrincipal]

    def get(self, request, student_id):
        student = get_object_or_404(Student, id=student_id)
        marks = Mark.objects.filter(student=student).select_related('subject')

        # Create response and canvas
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="report_card_{student_id}.pdf"'
        p = canvas.Canvas(response, pagesize=A4)
        p.setFont("Helvetica", 12)

        # Title
        p.drawString(100, 800, f"Report Card - {student.user.get_full_name()}")
        p.drawString(100, 780, f"Roll Number: {student.roll_number}")
        p.drawString(100, 760, f"Class: {student.class_name}")

        # Table headers
        y = 720
        p.drawString(100, y, "Subject")
        p.drawString(300, y, "Marks Obtained")
        y -= 20

        total = 0
        for mark in marks:
            p.drawString(100, y, mark.subject.name)
            p.drawString(300, y, str(mark.marks_obtained))
            total += mark.marks_obtained
            y -= 20

        subject_count = marks.count()
        if subject_count:
            avg = total / subject_count
        else:
            avg = 0

        # Total and average
        y -= 10
        p.drawString(100, y, f"Total: {total}")
        y -= 20
        p.drawString(100, y, f"Average: {avg:.2f}")

        # Finalize PDF
        p.showPage()
        p.save()
        return response

class ClassPerformanceView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsPrincipal]

    def list(self, request):
        data = (
            Mark.objects
            .values('student__standard__name')
            .annotate(avg_marks=Avg('marks_obtained'))
            .order_by('student__standard__name')
        )
        return Response(data)
    
class TopPerformersView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsPrincipal]

    def list(self, request):
        toppers = (
            Mark.objects
            .values('student_id', 'student__user__first_name', 'student__standard__name')
            .annotate(avg_marks=Avg('marks_obtained'))
            .order_by('-avg_marks')[:3]
        )
        return Response(toppers)

