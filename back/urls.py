from django.urls import path, include
from authentication.views import StudentRegistrationView, UserLoginView,ParentRegistrationView,TeacherRegistrationView,OrthoRegistrationView
from django.contrib import admin

from course.views import CourseListCreateAPIView, CourseRetrieveUpdateDestroyAPIView, ReviewListCreateAPIView, \
    ReviewRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/student/register/', StudentRegistrationView.as_view(), name='Student-registration'),
    path('api/parent/register/', ParentRegistrationView.as_view(), name='Parent-registration'),
    path('api/teacher/register/', TeacherRegistrationView.as_view(), name='Teacher-registration'),
    path('api/ortho/register/', OrthoRegistrationView.as_view(), name='Ortho-registration'),
    path('api/auth/login/', UserLoginView.as_view(), name='user-login'),
    path('api/courses/', CourseListCreateAPIView.as_view(), name='course-list'),
    path('api/courses/<int:pk>/', CourseRetrieveUpdateDestroyAPIView.as_view(), name='course-detail'),
    path('api/reviews/', ReviewListCreateAPIView.as_view(), name='review-list'),
    path('api/reviews/<int:pk>/', ReviewRetrieveUpdateDestroyAPIView.as_view(), name='review-detail'),]
