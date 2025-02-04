from django.contrib import admin
from django.urls import path, include
from api import *
from .views import *

urlpatterns = [
    path('registration/', UserRegistrationAPIView.as_view(), name='registration'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('user/<pk>/', UserDetailsAPIView.as_view()),

    path('addCourse/', AddCourseAPIView.as_view(), name='add-course'),


    path('courses/', CourseListAPIView.as_view()),
    path('courses/<pk>/', CourseDetailAPIView.as_view()),
    path('courses/<pk>/enroll/', EnrollCourseAPIView.as_view()),

    path('courses/<pk>/enrolled/', EnrolledCourseAPIView.as_view()),


    path('course-module/<course_id>/', CourseModuleDetailView.as_view()),

    path('logout/', LogoutAPIView.as_view()),



    path('forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot_password'),
    path('reset-password/', VerifyOTPAPIView.as_view(), name='reset-password'),

   ]
