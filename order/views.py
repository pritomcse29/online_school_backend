from order.serializers import EnrollmentSerializer,EnrollmentItemSerializer,OrderSerializer,ReviewSerializer
from course.serializers import CourseSerializer
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
from decimal import Decimal
from sslcommerz_lib import SSLCOMMERZ 
from django.conf import settings as main_settings
from django.http import HttpResponseRedirect
# Create your views here.
@api_view(['POST'])

def Enrollment_view_create(request):
    """
      This is enrollment page 
        - Where a login user enroll a course.
        - Others person has not access this page
    """
    if not request.user.is_authenticated or not request.user.groups.filter(name='student').exists():
        return Response({'message':'Only Students can enroll courses'}, status=status.HTTP_403_FORBIDDEN)

    data = request.data.get("courses", [])
    if not data:
        return Response({'message':'No course provided'}, status=status.HTTP_400_BAD_REQUEST)

    # Get or create a single cart per user
    enrollment, created = Enrollment.objects.get_or_create(student=request.user)

    # Add each course into the enrollment/cart
    for item in data:
        course_id = item.get("course")
        quantity = item.get("quantity", 1)
        price =  item.get("price")
        total_price = item.get("total_price")

        # Skip duplicates
        if EnrollmentItem.objects.filter(enroll=enrollment, course_id=course_id).exists():
            continue
        try:
            course = Course.objects.get(id=course_id)
            price = course.price  # Assuming Course model has a 'price' field
            total_price = Decimal(price) * int(quantity)
        except Course.DoesNotExist:
            continue  # Or return error if strict

        EnrollmentItem.objects.create(
            enroll=enrollment,
            course=course,
            quantity=quantity,
            price=price,
            total_price=total_price
        )

    serializer = EnrollmentSerializer(enrollment)
    #     EnrollmentItem.objects.create(
    #         enroll=enrollment,
    #         course_id=course_id,
    #         quantity=quantity,
    #         price = price,
    #         total_price = total_price
    #     )
    # serializer = EnrollmentSerializer(enrollment)
    return Response({
        "message": "Courses added to your cart",
        "cart_id": serializer.data
    }, status=status.HTTP_201_CREATED)

# @api_view(['POST'])
# def Enrollment_view_create(request):
#     # user = request.data
#     # is_student = request.user.groups.filter(name='student').exists()
#     if not request.user.is_authenticated or not request.user.groups.filter(name='student').exists():
#         return Response({'message':'Only Student can enroll course'},status=status.HTTP_204_NO_CONTENT)
#     data = request.data.get("courses",[])

#     if not data:
#         return Response({'message':'No course Provided'}) 
    
#     enrollment,created = Enrollment.objects.get_or_create(student=request.user)


#     serializer = EnrollmentSerializer(data=request.data,context={'request':request})
#     if serializer.is_valid():
#         enrollment = serializer.save()
#         return Response ({
#             "message":"Enrollment cart is created",
#             "cart id":str(enrollment.id),
            
#         },status=status.HTTP_201_CREATED)
    
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
def Enrollment_view(request):

    if not request.user.is_authenticated or not request.user.groups.filter(name= 'student').exists():
        return Response ({'message':'Only Student can view this'},status=status.HTTP_204_NO_CONTENT)
    enrollment = Enrollment.objects.filter(student = request.user).order_by('-enrolled_at')

    if not enrollment.exists():
         return Response ('No Course In this cart', status=status.HTTP_404_NOT_FOUND)
    serializer = EnrollmentSerializer(enrollment,many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['DELETE'])
def Enrollment_Delete_view(request, pk):
    if not request.user.is_authenticated or not request.user.groups.filter(name='student').exists():
        return Response({'message': 'Only Students can perform this action.'}, status=status.HTTP_403_FORBIDDEN)

    try:
        enrollment = EnrollmentItem.objects.get(id=pk, enroll__student=request.user)
    except Enrollment.DoesNotExist:
        return Response({'message': 'Enrollment not found.'}, status=status.HTTP_404_NOT_FOUND)

    enrollment.delete()
    return Response({'message': 'Enrollment deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


# @api_view(['DELETE'])
# def Enrollment_Delete_view(request, pk):
#     if not request.user.is_authenticated or not request.user.groups.filter(name='student').exists():
#         return Response({'message': 'Only students can delete enrollments.'}, status=status.HTTP_403_FORBIDDEN)

#     try:
#         enrollment = Enrollment.objects.get(student=request.user, id=pk)
#     except Enrollment.DoesNotExist:
#         return Response({'message': 'Enrollment not found.'}, status=status.HTTP_404_NOT_FOUND)

#     enrollment.delete()
#     return Response({'message': 'Enrollment deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


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
            # enrollment.enrollments.all().delete()
            # enrollment.status = Enrollment.CONFIRMED
            # enrollment.save()
            enrollment.enrollments.all().delete()
            # enrollment.items.all().delete()
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

@api_view(['PATCH'])
def cancel_order(request, order_id):
    if not request.user.is_authenticated or not request.user.groups.filter(name='student').exists():
        return Response({'message': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        order = Order.objects.get(id=order_id, student=request.user)
    except Order.DoesNotExist:
        return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if order.status != Order.PENDING:
        return Response({'message': 'Only pending orders can be cancelled'}, status=status.HTTP_400_BAD_REQUEST)

    order.status = Order.CANCELED
    order.save()
    return Response({'message': 'Order cancelled successfully'}, status=status.HTTP_200_OK)
    

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
    # all_order = Order.objects.all()
    if not filter_records.exists():
        return Response({"message":"There is no order record about seven days ago"})
    if not filters_records_thirty.exists():
        return Response({"message":"There is no order record about thirty days ago"})
    serializer_7 = OrderSerializer(filter_records,many=True)
    serializer_30 = OrderSerializer(filters_records_thirty,many=True)
    data={
        # "all_order":all_order,
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

@api_view(['GET'])
def teacher_dashboard_view(request):
    if not request.user.groups.filter(name='teacher').exists():
        return Response({'msg': 'Unauthorized'}, status=403)
    
    courses = Course.objects.filter(owner=request.user)
    serializer = CourseSerializer(courses, many=True)

    return Response({
        "my_courses": serializer.data,
        "total_courses": courses.count()
    })

@api_view(['GET'])
def student_dashboard_view(request):
    if not request.user.groups.filter(name='student').exists():
        return Response({'msg': 'Unauthorized'}, status=403)

    orders = Order.objects.filter(student=request.user)
    serializer = OrderSerializer(orders, many=True)
    return Response({
        "my_orders": serializer.data,
        "order_count": orders.count()
    })
@api_view(['POST'])
def add_course_view(request):
    if not request.user.groups.filter(name='teacher').exists():
        return Response({'msg': 'Unauthorized'}, status=403)

    serializer = CourseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)  # Automatically assign teacher
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PATCH'])
def admin_update_order_status(request, order_id):
    if not request.user.groups.filter(name='admin').exists():
        return Response({'msg': 'Forbidden'}, status=403)

    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({'msg': 'Order not found'}, status=404)

    status_val = request.data.get('status')
    if status_val not in [Order.CONFIRMED, Order.CANCELED]:
        return Response({'msg': 'Invalid status'}, status=400)

    order.status = status_val
    order.save(update_fields=['status'])
    return Response({'msg': 'Order status updated'})


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


@api_view(['POST'])
def initiate_payment(request):
    print(request.data)
    user = request.user
    amount = request.data.get("amount") 
    order_id = request.data.get("order_id")   
    print(user)
    # num_items = request.data.get("numItems")
    settings = { 'store_id': 'onlin6876330805605', 'store_pass': 'onlin6876330805605@ssl', 'issandbox': True }
    sslcz = SSLCOMMERZ(settings)
    post_body = {}
    post_body['total_amount'] = amount
    post_body['currency'] = "BDT"
    post_body['tran_id'] = f"txn_{order_id}"
    # post_body['success_url'] = "http://localhost:5173/dashboard/payment/success"
    post_body['success_url'] = f"{main_settings.BACKEND_URL}/api/v1/payment/success/"
    post_body['fail_url'] = f"{main_settings.BACKEND_URL}/api/v1/payment/fail/"
    post_body['cancel_url'] = f"{main_settings.BACKEND_URL}/api/v1/payment/cancel/"
    post_body['emi_option'] = 0
    post_body['cus_name'] = f"{user.first_name} {user.last_name}"
    post_body['cus_email'] = user.email
    post_body['cus_phone'] = user.number
    post_body['cus_add1'] = user.address
    post_body['cus_city'] = "Dhaka"
    post_body['cus_country'] = "Bangladesh"
    post_body['shipping_method'] = "No"
    post_body['multi_card_name'] = ""
    # post_body['num_of_item'] = num_items
    post_body['product_name'] = "E-Commerce Products"
    post_body['product_category'] = "General"
    post_body['product_profile'] = "general"
    post_body['ship_name'] = f"{user.first_name} {user.last_name}"

    response = sslcz.createSession(post_body) # API response
    # print(response)

    if response.get("status")=='SUCCESS':
       return Response({"payment_url":response['GatewayPageURL']})
    return Response({"error":"Payment initiation failed"},status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def payment_success(request):
    print("Inside success")
    order_id = request.data.get("tran_id").split('_')[1]
    order = Order.objects.get(id=order_id)
    order.status = "Confirmed"
    order.save()
    return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/dashboard/order/")


@api_view(['POST'])
def payment_cancel(request):
    return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/dashboard/order/")


@api_view(['POST'])
def payment_fail(request):
    print("Inside fail") 
    return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/dashboard/order/")