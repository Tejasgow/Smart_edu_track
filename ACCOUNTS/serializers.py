from rest_framework import serializers
from .models import user
from django.contrib.auth import authenticate
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator

class CreateUserserializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model=user
        fields=['username','email','password','role','first_name','last_name']

    def validate_role(self,value):
        if value not in ['teacher','parent']:
            raise serializers.ValidationError("Role must be teacher or parent.")
        return value
    
    def create(self,validated_data):
        password = validated_data.pop('password')
        users = user(**validated_data)
        users.set_password(password)
        users.save()
        return users


class CreateStudentSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = user
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'password']

    def validate_role(self, value):
        if value != 'student':  
            raise serializers.ValidationError("Role student")
        return value
    def create(self, validated_data):   
        password = validated_data.pop('password')
        users = user(**validated_data)
        users.set_password(password)   
        users.save()
        return users
    


class SessionLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid credentials")

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")

        data['user'] = user
        return data
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = user.objects.get(email=value)
        except user.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return value
    
class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            uid = force_str(urlsafe_base64_decode(data('uid')))
            users = user.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, user.DoesNotExist):
            raise serializers.ValidationError("Invalid UID.")
        if not default_token_generator.check_token(users, data['token']):
            raise serializers.ValidationError("Invalid or expired token.")
        
        data['user'] = users
        return data
    
    def save(self):
        users = self.validated_data['user']
        new_password = self.validated_data['new_password']
        users.set_password(new_password)
        users.save()
        return users