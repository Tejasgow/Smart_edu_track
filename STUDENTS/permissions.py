from rest_framework import permissions
from .models import ParentStudent,Student

class IsParentOrStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        student = getattr(obj, 'student', None)
        if student is None and isinstance(obj, Student):
            student = obj

        if student is None:
            return False

        if hasattr(student, 'user') and student.user == user:
            return True

        linked = ParentStudent.objects.filter(parent=user, student=student).exists()
        if linked:
            return True

        if user.is_staff:
            return True

        return False