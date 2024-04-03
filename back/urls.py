from django.urls import path, include
from authentication.views import UserRegistrationView, UserLoginView, UserLogoutView
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),  # Add this line to include admin URLs
    path('api/auth/register/', UserRegistrationView.as_view(), name='user-registration'),
    path('api/auth/login/', UserLoginView.as_view(), name='user-login'),
    path('api/auth/logout/', UserLogoutView.as_view(), name='user-logout'),
]
