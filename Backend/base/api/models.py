from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
import uuid

class User(models.Model):
    id = models.AutoField(primary_key=True)
    user_ref_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    full_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    mobile_no = models.CharField(max_length=50, null=True, blank = True)
    password = models.CharField(max_length=250)
    is_active = models.BooleanField(default=False)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=256 , null=True, blank=True)
    otp_expiry_time = models.DateTimeField(blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile_no']

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True
    
    def name(self):
        return self.full_name

    def __str__(self):
        return self.email

    class Meta:
        db_table = "users"


class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_ref_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=2000, null=True, blank=True)
    image = models.CharField(max_length=150, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    trainer = models.CharField(max_length=100, null=True, blank=True)
    parts = models.IntegerField(null=True, blank=True)
    
    def name(self):
        return self.title

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = "courses"

class CourseModule(models.Model):
    vedio_id = models.AutoField(primary_key=True)
    course_module_ref_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    course = models.ForeignKey(Course, to_field='course_ref_id', on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=500)
    video_link = models.URLField(max_length=2000)
    description = models.CharField(max_length=5000, null=True, blank=True)
    sequence = models.IntegerField()  

    def __str__(self):
        return f"{self.course.title} - {self.title}"
    
    class Meta:
        db_table = "course_module"

class StudentCourseEnrollment(models.Model):
    enrollment_id = models.AutoField(primary_key=True)
    enrollment_ref_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    student = models.ForeignKey(User, to_field='user_ref_id', on_delete=models.CASCADE, related_name='enrolled_courses')
    course = models.ForeignKey(Course, to_field='course_ref_id', on_delete=models.CASCADE, related_name='enrolled_students')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.email} - {self.course.title}"
    
    class Meta:
        db_table = "student_course_enrollment"
