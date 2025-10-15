from django.db import models
from ACCOUNTS.models import user

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
    users = models.OneToOneField(user, on_delete=models.CASCADE, related_name="student_profile")
    standard= models.ForeignKey(Standard, on_delete=models.SET_NULL,null=True)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.users.username 
    
class ParentStudent(models.Model):
    parent = models.ForeignKey(user , on_delete=models.CASCADE)
    student = models.ForeignKey("Student" , on_delete=models.CASCADE , related_name="parents")

    def __str__(self):
        return f"{self.parent.get_full_name()} = {self.student.users.get_full_name()}"


class Attendance(models.Model):
    student = models.ForeignKey(
        user,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "Student"},
        related_name="attendances"
    )
    date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=[("PRESENT", "Present"), ("ABSENT", "Absent")]
    )
    marked_by = models.ForeignKey(
        user,
        on_delete=models.SET_NULL,
        null=True,
        related_name="attendance_marked"
    )
    class Meta:
        unique_together = ("student", "date")
        ordering = ["-date"]

    def __str__(self):
        return f"{self.student.username} - {self.date} - {self.status}"
    
class Subject(models.Model):
    Sub_name = models.CharField(max_length=50)
    standard = models.ForeignKey(Standard,on_delete=models.CASCADE, related_name="subjects")
    teacher = models.ForeignKey(user,on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return f"{self.Sub_name} - {self.standard.name}"