from rest_framework import serializers
from .models import Mark, Exam


class MarkEntrySerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.get_full_name", read_only=True)
    subject_name = serializers.CharField(source="subject.name", read_only=True)

    class Meta:
        model = Mark
        fields = [
            'id', 'exam', 'student', 'student_name', 'subject', 'subject_name',
            'marks_obtained', 'max_marks', 'remarks', 'grade', 'updated_at'
        ]
        read_only_fields = ['grade', 'updated_at']

    def validate(self, data):
        if data['marks_obtained'] > data['max_marks']:
            raise serializers.ValidationError("Marks obtained cannot exceed max marks.")
        return data


class ExamSerializer(serializers.ModelSerializer):
    standard_name = serializers.CharField(source="standard.name", read_only=True)
    section_name = serializers.CharField(source="section.name", read_only=True)

    class Meta:
        model = Exam
        fields = ['id', 'name', 'date', 'standard', 'standard_name', 'section', 'section_name','created_by','created_at']
        read_only_fields=['created_by','created_at']

