from django.contrib import admin
from order.models import Enrollment,EnrollmentItem,Order,OrderItem
# Register your models here.
admin.site.register(Enrollment)
admin.site.register(EnrollmentItem)
admin.site.register(Order)
admin.site.register(OrderItem)
