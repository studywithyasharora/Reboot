from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from api import *
from .models import *
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from django.http import Http404
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.contrib.auth.models import User
from .email import send_otp
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def validate_user_input(full_name, email, mobile_no, password):
    if not full_name or not email or not mobile_no or not password:
        raise ValidationError("All fields are required")

    if User.objects.filter(email=email).exists():
        raise ValidationError("Email already exists")

    if User.objects.filter(mobile_no=mobile_no).exists():
        raise ValidationError("Mobile number already exists")
    

class UserRegistrationAPIView(APIView): 
    def post(self,request):
        try:
            full_name = request.data.get('full_name')
            email = request.data.get('email')
            mobile_no = request.data.get('mobile_no')
            password = request.data.get('password')

            validate_user_input(full_name, email, mobile_no, password)
            
            user_details = {
                "full_name" : full_name,
                "email" : email,
                "mobile_no":mobile_no,
                "password":make_password(password),
                "is_active":True,
                "is_verified":True
            }
            new_user = User.objects.create(**user_details)
            new_user.save()
            return Response({
                'status': 201,
                'message' : 'New user created succcessfully'
            })
        except ValidationError as e:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'error': str(e)
            })
        except Exception as e: 
            return Response({
                'status': 500,
                'error' : str(e)
            })
        
class UserLoginAPIView(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')

            if not email or not password:
                raise ValidationError("All fields are required")
            
            user_exists = User.objects.filter(email=email).values('id','user_ref_id','password')
            
            if user_exists:
                db_pass = user_exists[0]['password']
                check_pass = check_password(password, db_pass)

                if check_pass:
                    # user = user_exists.first()
                    user_id = user_exists[0]['id']
                    user_ref_id = user_exists[0]['user_ref_id']

                    user = get_object_or_404(User, id = user_id )

                    token = get_tokens_for_user(user)

                    return Response({
                        'status': 200,
                        'id': user_ref_id,
                        'token':token,
                        'message' : 'Log In succcessfully'
                    })
                else:
                    return Response({
                    'status': 401,
                    'message' : 'Wrong password'
                })
            else:
                return Response({
                    'status': 404,
                    'message' : 'User not found'
                })
        except ValidationError as e:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'error': e
            })
        except Exception as e: 
            return Response({
                'status': 500,
                'error' : str(e)
            })


class UserDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        try:
            user = User.objects.get(user_ref_id=pk)
            data = {'name': user.full_name, 'mobile_no': user.mobile_no, 
                'email': user.email}
            return Response({
                    'status': 200,
                    'data' : data
                })
        except Course.DoesNotExist:
            raise Http404


class AddCourseAPIView(APIView): 
    def post(self,request):
        try:
            title = request.data.get('title')
            description = request.data.get('description')
            image = request.data.get('image')
            category = request.data.get('category')
            trainer = request.data.get('trainer')
            parts = request.data.get('parts')
            price = request.data.get('price')

            # validate_user_input(full_name, email, mobile_no, password)
            
            user_details = {
                "title" : title,
                "description" : description,
                "image":image,
                "trainer" : trainer,
                "price" : price,
                "parts":parts,
                "category":category
            }
            new_user = Course.objects.create(**user_details)
            new_user.save()
            return Response({
                'status': 201,
                'message' : 'Created succcessfully'
            })
        except ValidationError as e:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'error': str(e)
            })
        except Exception as e: 
            return Response({
                'status': 500,
                'error' : str(e)
            })
        

class CourseListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            courses = Course.objects.all()
            data = [{'id': course.course_ref_id, 'title': course.title, 
                    'image':course.image, 
                    'price': course.price, 'category': course.category, 
                    } for course in courses]
            return Response({
                    'status': 200,
                    'data' : data
                })
        except Course.DoesNotExist:
            raise Http404

class CourseDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        try:
            course = Course.objects.get(course_ref_id=pk)
            data = {'id': course.course_ref_id, 'title': course.title, 
                'description': course.description, 'image':course.image, 
                'price': course.price, 'category': course.category, 
                'trainer': course.trainer, 'parts': course.parts 
                }
            return Response({
                    'status': 200,
                    'data' : data
                })
        except Course.DoesNotExist:
            raise Http404

class CourseModuleDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, course_id):
        try:
            print(course_id)
            course_modules = CourseModule.objects.filter(course_id=course_id)
            data = []
            for module in course_modules:
                module_data = {
                    'vedio_id': module.course_module_ref_id,
                    'title': module.title,
                    'video_link': module.video_link,
                    'description': module.description,
                    'sequence': module.sequence,
                }
                data.append(module_data)
            return Response({
                    'status': 200,
                    'data' : data
                })
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        

class EnrollCourseAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        try:
            course = Course.objects.get(course_ref_id=pk)
            enrollment, created = StudentCourseEnrollment.objects.get_or_create(student=request.user, course=course)
            if created:
                return Response({
                    'status': 201,
                    'message': 'Enrolled successfully'
                })
            return Response({
                    'status': 200,
                    'message': 'Already enrolled'
                })
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class EnrolledCourseAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        try:
            courses = StudentCourseEnrollment.objects.filter(student=pk).select_related(
                    'course').order_by('-enrolled_at')

            data = []
            for details in courses:
                data.append({
                    'id': details.enrollment_ref_id,
                    'timestamp': details.enrolled_at,
                    'course': {
                        'id': details.course.course_ref_id,
                        'title': details.course.title,
                        'image': details.course.image,

                    }
                })
            return Response({
                    'status': 200,
                    'data' : data
                })
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            if refresh_token:
                access = RefreshToken(refresh_token)
                access.blacklist()
                return Response({
                    'status':200,
                    'message':'success',
                    'data':'Logged out',
                })
            else:
                return Response({
                'status':400,
                'message':'Failed',
                'data':'failed',
            })
        except Exception as e:
            return Response({"detail": f"Error during logout: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        







class ForgotPasswordAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.filter(email=email).values('user_ref_id')
            if user:
                user_ref_id = user[0]['user_ref_id']
                send_otp(email)
                return Response({
                    'status':200,
                    'message':'OTP sent',
                    'id': user_ref_id,
                })
            return Response({
                    'status':400,
                    'message':'Email not found',
                })
        except Exception as e:
            return Response({
                'status':500,
                'message':str(e)
            })

class VerifyOTPAPIView(APIView):
    def post(self, request):
        try:
            user_ref_id = request.data.get('user_ref_id')
            otp = request.data.get('otp')
            password = request.data.get('password')
            if user_ref_id and otp and password:
                user = User.objects.filter(user_ref_id = user_ref_id).values("otp","otp_expiry_time")
                
                user_otp = user[0]['otp']
                user_otp_exp_time = user[0]['otp_expiry_time']
                
                if (check_password(otp, user_otp) and user_otp_exp_time > timezone.now() ):
                    user.update(password=password)

                    return Response({
                    'status' : 200,
                    'message' : 'Password reset successfull',
                })
                else:
                    return Response({
                        'status':400,
                        'message': 'something went wrong',
                        'data' : "Wrong OTP or OTP expired",
                    })
        except Exception as e:
            return Response({
                'status':500,
                'message': str(e),
            })



