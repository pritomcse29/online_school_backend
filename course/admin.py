from django.contrib import admin
from course.models import Course,Subject,CourseImage,SubjectImage
# Register your models here.
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(CourseImage)
admin.site.register(SubjectImage)
