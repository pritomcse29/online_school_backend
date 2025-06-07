from django.db import models
from django.conf import settings
import uuid
from uuid import uuid4
from course.models import Course
from decimal import Decimal
# Create your models here.
class Enrollment(models.Model):
    # PENDING='Pending'
    # CONFIRMED='Confirmed'
    # CANCELED='Canceled'

    # STATUS_CHOICES =[
    #     (PENDING,'Pending'),
    #     (CONFIRMED,'Confirmed'),
    #     (CANCELED,'Canceled'),
    # ]
   
    id = models.UUIDField(primary_key=True,default=uuid4,editable=False)
    student = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='students')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    # status = models.CharField(choices=STATUS_CHOICES,max_length=20,default=PENDING)
    def __str__(self):
        return f"Enrollment of {self.student.first_name} {self.student.last_name}"

class EnrollmentItem(models.Model):
    enroll = models.ForeignKey(Enrollment,on_delete=models.CASCADE,related_name='enrollments')
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        unique_together = ['course','quantity']

    def __str__(self):
        return f"{self.course} x {self.quantity}"
    
class Order(models.Model):
    PENDING ='Pending'
    CONFIRMED = 'Confirmed'
    CANCELED = 'Canceled'
    
    STATUS_CHOICES =[
        (PENDING,'Pending'),
        (CONFIRMED,'Confirmed'),
        (CANCELED,'Canceled')
    ]

    id = models.UUIDField(default=uuid4,editable=False,primary_key=True)
    student = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES,default=PENDING,max_length=20)
    total_price = models.DecimalField(max_digits=10,decimal_places=2,default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order for {self.student.first_name} - Order Id {self.id}"
class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='orders')
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='order_courses')
    price = models.DecimalField(max_digits=10,decimal_places=2,default=Decimal('0.00'))
    quantity = models.IntegerField()
    total_price  = models.DecimalField(max_digits=10,decimal_places=2,default=Decimal('0.00'))

    @property
    def calculate_total_price(self):
        return self.price * self.quantity
    
    def save(self, *args, **kwargs):
        self.total_price = self.calculate_total_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.course.name}"
    
class Review(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return f"Comment By {self.student.first_name} - for {self.course.name} Course"
    
class adminTeacher(models.Model):
    name = models.CharField(max_length=50)
    designation = models.CharField(max_length=100)
    





