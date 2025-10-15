from django.urls import path
from . import views

urlpatterns = [    
    path('marks/entry/', views.MarkEntryListCreateView.as_view(), name='mark-entry'),
    path('exams/', views.ExamListCreateView.as_view(), name='exam-list-create'),
]
