from rest_framework import serializers
from ACCOUNTS.models import User
from .models import Student, Standard , Section , ParentStudent



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

        users = User.objects.create(
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
        fields = ['id','parent_id','student_id']


    def validate(self,data):
        try:
            parent = User.objects.get(id=data['parent_id'],role="parent")
        except User.DoesNotExist:
            raise serializers.ValidationError("invalid parent_id or user is not a perfect")
        try:
            student = Student.objects.get(id=data["student_id"])
        except Student.DoesNotExist:
            raise serializers.ValidationError("invalid student_id")
        return data
    

    def create(self,validated_data):
        parent = User.objects.get(id=validated_data['parent_id'])
        student = Student.objects.get(id=validated_data['student_id'])
        link , created = ParentStudent.objects.get_or_create(parent=parent , student=student)
        return link
    
    def to_representation(self, instance):
        return{
            "link_id":instance.id,
            "student":instance.student.users.first_name,
            "parent":instance.parent.first_name,
            "message":"parent linked to student successfully"

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

