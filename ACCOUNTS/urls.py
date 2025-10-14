from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView
urlpatterns = [
    path('createteacherparent/',views.createTeacherParentView.as_view()),
    path('login/',csrf_exempt(views.sessionloginview.as_view()),name="session-login"),
    path('logout/',views.sessionlogoutview.as_view(),name="session-logout"),
    path('PasswordReset/',views.PasswordResetRequestView.as_view(),name="ResetPassword"),
    path('PasswordCofirm/',views.PasswordResetConfirmView.as_view(),name="ConfirmPassword"),
    path('gettoken/', TokenObtainPairView.as_view(), name='token_obtain_pair'),   # Login
    path('token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh
    path('token-verify/', TokenVerifyView.as_view(), name='token_verify'),      # 👈 Verify Token
]

