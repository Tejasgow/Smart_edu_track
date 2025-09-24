from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('createteacherparent/',views.createTeacherParentView.as_view()),
    path('login/',csrf_exempt(views.sessionloginview.as_view()),name="session-login"),
    path('logout/',views.sessionlogoutview.as_view(),name="session-logout"),
    path('PasswordReset/',views.PasswordResetRequestView.as_view(),name="ResetPassword"),
    path('PasswordCofirm/',views.PasswordResetConfirmView.as_view(),name="ConfirmPassword"),
]
