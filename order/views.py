from order.serializers import EnrollmentSerializer,EnrollmentItemSerializer,OrderSerializer,ReviewSerializer
from order.models import Enrollment,EnrollmentItem,Order,OrderItem,Review,Course
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import transaction
from datetime import datetime,timedelta
from django.utils.timezone import now
from rest_framework.viewsets import ModelViewSet
from django.conf import settings
from .serializers import adminTeacherSerializer
from users.models import User
from course.models import Course,Subject
# Create your views here.

@api_view(['POST'])
def Enrollment_view_create(request):
    # user = request.data
    # is_student = request.user.groups.filter(name='student').exists()
    if not request.user.is_authenticated or not request.user.groups.filter(name='student').exists():
        return Response({'message':'Only Student can enroll course'},status=status.HTTP_204_NO_CONTENT)
    serializer = EnrollmentSerializer(data=request.data,context={'request':request})
    if serializer.is_valid():
        enrollment = serializer.save()
        return Response ({
            "message":"Enrollment cart is created",
            "cart id":str(enrollment.id),
            
        },status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
def Enrollment_view(request):
    if not request.user.is_authenticated or not request.user.groups.filter(name= 'student').exists():
        return Response ({'message':'Only Student can view this'},status=status.HTTP_204_NO_CONTENT)
    enrollment = Enrollment.objects.filter(student = request.user).order_by('-enrolled_at')

    if not enrollment.exists():
         return Response ('No Course In this cart', status=status.HTTP_404_NOT_FOUND)
    serializer = EnrollmentSerializer(enrollment,many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def Order_view(request):
    if not request.user.is_authenticated or not request.user.groups.filter(name='student').exists():
        return Response({'message':'Only Student Can view this order'},status=status.HTTP_204_NO_CONTENT)
    enrollment_id = request.data.get('enrollment_id')
    if not enrollment_id:
        return Response({"error": "enrollment_id is required"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        enrollment = Enrollment.objects.get(id=enrollment_id,student=request.user)
    except Enrollment.DoesNotExist:
        return Response({"error": "Cart not found or already confirmed"}, status=status.HTTP_404_NOT_FOUND)
    order_data = {
        "items": [{
            "course": item.course.id, 
            "quantity": item.quantity,
            "price": item.course.price,       
            "total_price": item.course.price * item.quantity
            } for item in enrollment.enrollments.all()]
    }
    if not order_data['items']:
        return Response({"error": "No courses in cart"}, status=status.HTTP_400_BAD_REQUEST)

    serializer = OrderSerializer(data=order_data, context={'request': request})
    if serializer.is_valid():
        with transaction.atomic():
            order = serializer.save()
            # enrollment.status = Enrollment.CONFIRMED
            # enrollment.save()
        return Response({
            "message": "Order created successfully",
            "order_id": str(order.id),
            "enrollment_id": str(enrollment.id)
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def order_view_set(request):
    if not request.user.is_authenticated or not request.user.groups.filter(name__in=["student","admin"]).exists():
           return Response({'message':"Only owner of this order can view this"},status=status.HTTP_403_FORBIDDEN)
    order = Order.objects.filter(student=request.user).order_by('-created_at')
    if not order:
        return Response({'message':"There is no order found"},status=status.HTTP_204_NO_CONTENT)
    serializer = OrderSerializer(order,many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def admin_view_set(request):
    if not request.user.is_authenticated or not request.user.groups.filter(name="admin").exists():
        return Response({"message":"only admin can view this"},status=status.HTTP_403_FORBIDDEN)
    course_count = Course.objects.count()
    subject_count = Subject.objects.count()
    total_mentor =  User.objects.filter(groups__name="teacher").count()
    total_student =  User.objects.filter(groups__name="student").count()
    seven_days_ago =  now()-timedelta(days=7)
    thirty_days_ago = now() - timedelta(days=30)
    filter_records = Order.objects.filter(created_at__gt = seven_days_ago)
    filters_records_thirty = Order.objects.filter(created_at__gt = thirty_days_ago)
    if not filter_records.exists():
        return Response({"message":"There is no order record about seven days ago"})
    if not filters_records_thirty.exists():
        return Response({"message":"There is no order record about thirty days ago"})
    serializer_7 = OrderSerializer(filter_records,many=True)
    serializer_30 = OrderSerializer(filters_records_thirty,many=True)
    data={
        "last_7_days_orders":serializer_7.data,
        "last_30_days_orders":serializer_30.data,
        "Total_Course":course_count,
        "Total_Subject":subject_count,
        "Total_Mentor":total_mentor,
        "Total_Student":total_student,
    }
    return Response(data,status=status.HTTP_200_OK)    

@api_view(['GET'])
def count_view_set(request):

    course_count = Course.objects.count()
    subject_count = Subject.objects.count()
    total_mentor =  User.objects.filter(groups__name="teacher").count()
    total_student =  User.objects.filter(groups__name="student").count()

    data={
        "Total_Course":course_count,
        "Total_Subject":subject_count,
        "Total_Mentor":total_mentor,
        "Total_Student":total_student,
    }
    return Response(data,status=status.HTTP_200_OK)   

# @api_view(['POST'])
# def review_create(request):
#     if not request.user.is_authenticated or not request.user.groups.filter(name__in=['admin','student']).exists():
#         return Response({"message":"Only admin and Student can create review"},status=status.HTTP_404_NOT_FOUND)
#     course_id = request.data.get('course_id')
#     student = request.context['request'].user
#     data={
#         "course_id":course_id,
#         "student":student
#     }
#     serializer = ReivewSerializer(data=request.data,context={'request':request})
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data,status=status.HTTP_201_CREATED)
#     return Response(serializer.errors,status=status.HTTP_403_FORBIDDEN)

# @api_view(['POST'])
# def review_create(request):
#     if not request.user.is_authenticated or not request.user.groups.filter(name__in=['admin','student']).exists():
#         return Response({"message": "Only admin and Student can create review"}, status=status.HTTP_403_FORBIDDEN)

#     course_id = request.data.get('course_id')
#     if not course_id:
#         return Response({"error": "course_id is required"}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         course = Course.objects.get(id=course_id)
#     except Course.DoesNotExist:
#         return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
#     data = request.data.copy()
#     data.pop('course_id', None)
#     serializer = ReivewSerializer(data=data, context={'request': request,'course':course})
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class reviewCreate(ModelViewSet):
#     """
#     Handles reviews for a specific product.
#     """
#     serializer_class = ReivewSerializer

#     def get_queryset(self):
#         return Review.objects.filter(course_id=self.kwargs.get('course_pk'))

#     def get_serializer_context(self):
#         return {'course_id': self.kwargs.get('course_pk')}

class reviewCreate(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(course_id=self.kwargs.get('course_pk'))

    def get_serializer_context(self):
        context = super().get_serializer_context()
        return context
@api_view(['GET'])
def adminTeacherView(request):
    data = User.objects.filter(groups__name__in=["admin","teacher"])
    serializer = adminTeacherSerializer(data,many = True)
    return Response(serializer.data, status=status.HTTP_200_OK)

    # if serializer.is_valid():

    #     serializer.save()
    #     return Response(serializer.data,status=status.HTTP_200_OK)
    # return Response(serializer.errors,status=status.HTTP_403_FORBIDDEN)





