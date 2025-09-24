from django.db import models
from ACCOUNTS.models import User

# Create your models here.

class Standard(models.Model):
    name=models.CharField(max_length=20,unique=True)

    def __str__(self):
        return self.name
    

class Section(models.Model):
    name=models.CharField(max_length=20)
    standard = models.ForeignKey(Standard,on_delete=models.CASCADE, related_name="sections")

    def __str__(self):
        return f"{self.standard.name} - {self.name}"
    

class Student(models.Model):
    users = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    standard= models.ForeignKey(Standard, on_delete=models.SET_NULL,null=True)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.users.username 
    


class ParentStudent(models.Model):
    parent = models.ForeignKey(User , on_delete=models.CASCADE)
    student = models.ForeignKey("Student" , on_delete=models.CASCADE , related_name="parents")

    def __str__(self):
        return f"{self.parent.get_full_name()} = {self.student.User.get_full_name()}"