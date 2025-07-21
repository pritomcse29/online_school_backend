from .models import Enrollment,EnrollmentItem,Course,Order,OrderItem,Review
from rest_framework import serializers
from django.db import transaction
from order.models import adminTeacher
from users.models import User
class EnrollmentItemSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    course_details = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = EnrollmentItem
        fields =['id','course','course_details','quantity','total_price']
        read_only_fields =['id','course_details','total_price']

    def get_course_details(self,obj):
        return {"id":obj.course.id,"name":obj.course.name} 
    def get_total_price(self,obj):
        return obj.quantity * obj.course.price 
         
# Write-only serializer
class EnrollmentItemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrollmentItem
        fields = ['course', 'quantity']

# Updated EnrollmentSerializer
class EnrollmentSerializer(serializers.ModelSerializer):
    courses = EnrollmentItemWriteSerializer(many=True, write_only=True)
    enrollments = EnrollmentItemSerializer(many=True, read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'courses', 'enrollments', 'student', 'enrolled_at']
        read_only_fields = ['id', 'student', 'enrolled_at', 'enrollments']

    def validate(self, data):
        if not data.get("courses"):
            raise serializers.ValidationError("At least one course is required.")
        return data

    def create(self, validated_data):
        courses_data = validated_data.pop('courses')
        student = self.context['request'].user
        with transaction.atomic():
            enrollment = Enrollment.objects.create(student=student)
            for item in courses_data:
                EnrollmentItem.objects.create(
                    enroll=enrollment,
                    course=item['course'],
                    quantity=item.get('quantity', 1)
                )
        return enrollment


# class EnrollmentSerializer(serializers.ModelSerializer):
#     courses = EnrollmentItemSerializer(many=True, source='enrollments')
#     enrollments = EnrollmentItemSerializer(many=True, read_only=True)

#     class Meta:
#         model = Enrollment
#         fields = ['id', 'courses', 'enrollments', 'student','enrolled_at']
#         read_only_fields = ['id', 'student', 'enrolled_at', 'enrollments',]

#     def validate(self, data):
#         if not data.get("enrollments") and not data.get("courses"):
#             raise serializers.ValidationError("At least one course needed")
#         return data

#     def create(self, validated_data):
#         courses_data = validated_data.pop('enrollments', None) or validated_data.pop('courses')
#         student = self.context['request'].user
#         with transaction.atomic():
#             enrollment = Enrollment.objects.create(student=student)
#             for item in courses_data:
#                 clean_data = {
#                     "course": item["course"],
#                     "quantity": item.get("quantity", 1)
#                 }
#                 EnrollmentItem.objects.create(enroll=enrollment, **clean_data)

#     #         for course_data in courses_data:
#     #             # EnrollmentItem.objects.create(enroll=enrollment, **course_data)
#     #             EnrollmentItem.objects.create(
#     #     enroll=enrollment,
#     #     course=course_data["course"],
#     #     quantity=course_data.get("quantity", 1)
#     # )
#         return enrollment


# class EnrollmentSerializer(serializers.ModelSerializer):
#     # courses = EnrollmentItemSerializer(many=True,source='enrollments')
#     # courses = EnrollmentItemSerializer(many=True, source ='enrollments' )

#     enrollments = EnrollmentItemSerializer(many=True, read_only=True)


#     class Meta:
#         model =  Enrollment
#         fields =['id','enrollments','student','enrolled_at']
#         read_only_fields = ['id','student','enrolled_at']
#         # read_only_fields = ['id','courses','student','enrolled_at']

#     def validate(self,data):
#             if not data.get("enrollments"):
#                 raise serializers.ValidationError("At least one course needed")
#             return data
       
#     def create(self, validated_data):
#             courses_data = validated_data.pop('enrollments')
#             student = self.context['request'].user
#             with transaction.atomic():
#                 enrollment = Enrollment.objects.create(student=student)
#                 for course_data in courses_data:
#                     EnrollmentItem.objects.create(enroll=enrollment, **course_data)
#             return enrollment
class OrderItemSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    course_details = serializers.SerializerMethodField()
    class Meta:
        model = OrderItem
        fields =['id','course','price','quantity','total_price','course_details']
        read_only_fields = ['course','course_details','id']

    def get_course_details(self,obj):
             return {"id":obj.course.id,"name":obj.course.name}
        
    def create(self, validated_data):
             course = validated_data['course']
             validated_data['price'] = course.price
             validated_data['total_price'] =validated_data['price'] * validated_data['quantity']
             return super().create(validated_data)     
        
          
class OrderSerializer(serializers.ModelSerializer):
     items = OrderItemSerializer(many=True,source="orders")
     class Meta:
        model = Order
        fields = ['id', 'student', 'status', 'total_price', 'created_at', 'updated_at', 'items']
        read_only_fields = ['id', 'student', 'total_price', 'created_at', 'updated_at']

     def validated(self,data):
          if not data.get('items'):
               raise serializers.ValidationError("Minimum one Item must be needed")
          return data
     def create(self, validated_data):
        items_data = validated_data.pop('orders')
        student = self.context['request'].user
        with transaction.atomic():
            order = Order.objects.create(student=student, total_price=0)
            total = 0
            for item_data in items_data:
                item = OrderItem.objects.create(order=order, **item_data)
                total += item.total_price
            order.total_price = total
            order.save()
        return order
    #  def create(self,validated_data):
          
    #      items_data = validated_data.pop('items')
    #      student = self.context['request'].user
    #      with transaction.atomic():
    #           order = Order.objects.create(student=student,total_price =0)
    #           total = 0 
    #           for item_data in items_data:
    #                item = OrderItem.objects.create(order=order,**items_data)
    #                total+=item.total_price
    #           order.total_price = total
    #           order.save()
# class ReivewSerializer(serializers.ModelSerializer):
#      course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
#      class Meta:
#           model = Review
#           fields =["course","student","comment","rating"]
          

#      def create(self,validated_data):
#                course_id = self.context['course_id']
#             #    student = self.context['request'].user
            
#                review = Review.objects.create(course_id=course_id,**validated_data)
#             #    review = Review.objects.create(course=course, student=student,**validated_data)
#                return review

class ReviewSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = Review
        fields = ["course", "student", "comment", "rating"]
        read_only_fields = ['student'] 

    def create(self, validated_data):
        course = validated_data.pop('course', None)  
        student = self.context['request'].user      
        review = Review.objects.create(course=course, student=student, **validated_data)
        return review
class adminTeacherSerializer(serializers.ModelSerializer):
    group_names = serializers.SerializerMethodField()

    class Meta:
        model = User  # Or your custom user model
        fields = ['first_name', 'last_name', 'email', 'group_names']

    def get_group_names(self, obj):
        # This will return a list of group names for each user
        return [group.name for group in obj.groups.all()]




     