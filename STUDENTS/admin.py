from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(Standard)
class StandardAdmin(admin.ModelAdmin):
    list_display=['id','name']


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display=['id','name','standard']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display=['id','users','standard','section','created_at']