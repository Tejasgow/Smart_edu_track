from rest_framework import serializers
from .models import Exam, Mark

class markentrySerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.users.get_full_name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    class Meta:
        model = Mark
        fields = ['id', 'exam', 'student', 'student_name', 'subject', 'subject_name', 'marks_obtained', 'max_marks', 'remarks', 'grade', 'entered_by', 'updated_at']
        read_only_fields = ['grade', 'updated_at']

    def validate(self, data):
        if data['marks_obtained'] > data['max_marks']:
            raise serializers.ValidationError("Marks obtained cannot be greater than maximum marks")
        return data

class examSerializer(serializers.ModelSerializer):
    standard_name = serializers.CharField(source='standard.name', read_only=True)
    section_name = serializers.CharField(source='section.name', read_only=True)

    class Meta:
        model = Exam
        fields = [
            'id',
            'name',
            'date',
            'standard',
            'standard_name',
            'section',
            'section_name',
            'created_at',
            'created_by',
            ''
        ]
        read_only_fields = ['created_at', 'created_by']
