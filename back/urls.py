from django.urls import path, include
from authentication.views import StudentRegistrationView, UserLoginView, ParentRegistrationView, \
    TeacherRegistrationView, OrthoRegistrationView, UserLogoutView
from django.contrib import admin

from course.views import CourseListCreateAPIView, CourseRetrieveUpdateDestroyAPIView, ReviewListCreateAPIView, \
    ReviewRetrieveUpdateDestroyAPIView
from tti.views import  GenerateImageAPIView
from writting.views import predictFr, predictDigits, predictAr
from tts.views import  TextToSpeechAPI
from ocr.views import OCRView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/student/register/', StudentRegistrationView.as_view(), name='Student-registration'),
    path('api/parent/register/', ParentRegistrationView.as_view(), name='Parent-registration'),
    path('api/teacher/register/', TeacherRegistrationView.as_view(), name='Teacher-registration'),
    path('api/ortho/register/', OrthoRegistrationView.as_view(), name='Ortho-registration'),
    path('api/auth/login/', UserLoginView.as_view(), name='user-login'),
    path('api/auth/logout/',UserLogoutView.as_view(),name='user-logout'),
    path('api/courses/', CourseListCreateAPIView.as_view(), name='course-list'),
    path('api/courses/<int:pk>/', CourseRetrieveUpdateDestroyAPIView.as_view(), name='course-detail'),
    path('api/reviews/', ReviewListCreateAPIView.as_view(), name='review-list'),
    path('api/reviews/<int:pk>/', ReviewRetrieveUpdateDestroyAPIView.as_view(), name='review-detail'),
    path('api/Fr',predictFr.as_view(),name='pred'),
    path('api/Digits',predictDigits.as_view(),name='predD'),
    path('api/Arabe', predictAr.as_view(), name='predAr'),
    path('api/tti',GenerateImageAPIView.as_view(), name='tti'),
    path('api/tts', TextToSpeechAPI.as_view(), name='convert_to_speech'),
    path('api/ocr', OCRView.as_view(), name='ocr'),

]
