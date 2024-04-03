from django.urls import path, include
from authentication.views import StudentRegistrationView, UserLoginView,ParentRegistrationView,TeacherRegistrationView,OrthoRegistrationView
# UserLogoutView
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),  # Add this line to include admin URLs
    path('api/student/register/', StudentRegistrationView.as_view(), name='Student-registration'),
    path('api/parent/register/', ParentRegistrationView.as_view(), name='Parent-registration'),
    path('api/teacher/register/', TeacherRegistrationView.as_view(), name='Teacher-registration'),
    path('api/ortho/register/', OrthoRegistrationView.as_view(), name='Ortho-registration'),
    path('api/auth/login/', UserLoginView.as_view(), name='user-login'),

]
