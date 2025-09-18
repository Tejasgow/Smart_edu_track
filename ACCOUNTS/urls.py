from django.urls import path
from .views import CreateTeacherView
urlpatterns = [
    path('createTeacher/',CreateTeacherView.as_view(), name='createTeacher'),

]