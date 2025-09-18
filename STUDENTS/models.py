from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class StudentUser(AbstractUser):
    studentName = models.CharField(max_length=100)
    studentDOB = models.DateField()
    studentRegisterID = models.CharField(max_length=20, unique=True)
    studentClass = models.CharField(max_length=50)
    studentSection = models.CharField(max_length=10)
