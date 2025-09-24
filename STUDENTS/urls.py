from django.urls import path
from . import views
urlpatterns = [
    path('studentreg/',views.StudentRegistrationView.as_view()),
    path('isteacher/',views.IsTeacher),
    path('link/',views.LinkparentToStudentView.as_view()),
    path('standards/',views.StandardListCreatView.as_view(),name="views.StandardListCreatView"),
    path("sections/",views.SectionListCreateView.as_view(),name="views.SectionListCreateView"),
]