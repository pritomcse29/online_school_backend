from .models import Enrollment,EnrollmentItem,Course,Order,OrderItem
from rest_framework import serializers
from django.db import transaction

class EnrollmentItemSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    course_details = serializers.SerializerMethodField()

    class Meta:
        model = EnrollmentItem
        fields =['id','course','course_details','quantity']
        read_only_fields =['id','course_details']

    def get_course_details(self,obj):
        return {"id":obj.course.id,"name":obj.course.name} 
    
class EnrollmentSerializer(serializers.ModelSerializer):
    courses = EnrollmentItemSerializer(many=True,source='enrollments')
    class Meta:
        model =  Enrollment
        fields =['id','courses','student','enrolled_at']
        read_only_fields = ['id','courses','student','enrolled_at']

    def validate(self,data):
            if not data.get("courses"):
                raise serializers.ValidationError("At least one course needed")
            return data
       
    def create(self, validated_data):
            courses_data = validated_data.pop('courses')
            student = self.context['request'].user
            with transaction.atomic():
                enrollment = Enrollment.objects.create(student=student)
                for course_data in courses_data:
                    EnrollmentItem.objects.create(enroll=enrollment, **course_data)
            return enrollment
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
        items_data = validated_data.pop('items')
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


     