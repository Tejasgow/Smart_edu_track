from django.urls import path
from . import views
urlpatterns = [    
    path('report-card/<int:student_id>/', views.ReportCardView.as_view(), name='ReportCardView'),
    path('class-performance/', views.ClassPerformanceView.as_view(), name='ClassPerformanceView'),
    path('toppers/',views.TopPerformersView.as_view(),name='TopPerformersView')
]