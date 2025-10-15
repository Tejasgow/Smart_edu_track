from rest_framework import serializers
from ACCOUNTS.models import user
from .models import Student, Standard , Section , ParentStudent,Attendance,Subject



class StudentRegistrationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    standard_id = serializers.IntegerField(write_only=True)
    section_id = serializers.IntegerField(write_only=True)


    class Meta:
        model=Student
        fields = ['id', 'name', 'email', 'password', 'standard_id', 'section_id']


    def create(self, validated_data):

        users = user.objects.create(
            username = validated_data['email'],
            email = validated_data['email'],
            password = validated_data['password'],
            first_name= validated_data['name'],
            role='STUDENT'
        )


        standard = Standard.objects.get(id=validated_data['standard_id'])
        section = Section.objects.get(id=validated_data['section_id'])



        student=Student.objects.create(
            users=users,
            standard=standard,
            section=section,
        )
        return student
    
    def to_representation(self, instance):
        return {
            "student_id":instance.id,
            "name":instance.users.first_name,
            "email":instance.users.email,
            "standard":instance.standard.name if instance.standard else None,
            "section":instance.section.name if instance.section else None,
        }
    

class LinkParentSerializer(serializers.ModelSerializer):
    parent_id = serializers.IntegerField()
    student_id = serializers.IntegerField()

    class Meta:
        model = ParentStudent
        fields = ['id', 'parent_id', 'student_id']

    def validate(self, data):
        print("Received parent_id:", data.get('parent_id'))
        print("Received student_id:", data.get('student_id'))
        # Validate parent
        try:
            parent = user.objects.get(id=data['parent_id'], role="parent")
        except user.DoesNotExist:
            raise serializers.ValidationError({"parent_id": "Invalid parent_id or user is not a parent."})

        # Validate student
        try:
            student = Student.objects.get(id=data['student_id'])
        except Student.DoesNotExist:
            raise serializers.ValidationError({"student_id": "Invalid student_id."})

        # Inject validated model instances
        data['parent'] = parent
        data['student'] = student
        return data

    def create(self, validated_data):
        parent = validated_data['parent']
        student = validated_data['student']
        link, created = ParentStudent.objects.get_or_create(parent=parent, student=student)
        return link

    def to_representation(self, instance):
        return {
            "link_id": instance.id,
            "student": instance.student.users.first_name,  # ✅ fixed: 'user' not 'users'
            "parent": instance.parent.first_name,
            "message": "Parent linked to student successfully"
        }

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'

class StandardSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only = True)

    class Meta:
        model = Standard
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ["id", "student", "date", "status", "marked_by"]
        read_only_fields = ["id", "marked_by"]

class AttendanceMarkSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    date = serializers.DateField()
    status = serializers.ChoiceField(choices=[("PRESENT", "Present"), ("ABSENT", "Absent")])

    def validate_student_id(self, value):
        if not user.objects.filter(id=value, role="Student").exists():
            raise serializers.ValidationError("Student with this ID does not exist.")
        return value

class AttendanceDailySerializer(serializers.ModelSerializer):
    Student_name = serializers.StringRelatedField(source='Student.users.full_name', read_only=True)
    Standard = serializers.CharField(source='Student.standard.name', read_only=True)
    Section = serializers.CharField(source='Student.section.name', read_only=True)

    class Meta:
        model = Attendance
        fields =["id","Date","Status","Marked_by","Student_name","Standard","Section"]
        
class StudentAttendanceSummarySerializer(serializers.ModelSerializer):
  Student_name = serializers.StringRelatedField()
  Standard = serializers.CharField()
  Section = serializers.CharField()
  Total_Days_Present = serializers.IntegerField()
  Total_Days_Absent = serializers.IntegerField()
  Attendance_Percentage = serializers.FloatField()

class SubjectSerializer(serializers.ModelSerializer):   
    standard_name = serializers.CharField(source='standard.name', read_only=True)
    teacher_name = serializers.CharField(source='teacher.get_full_name', read_only=True)

    class Meta:
        model = Subject
        fields = ["id", "name", "code", "standard", "standard_name", "teacher", "teacher_name"]