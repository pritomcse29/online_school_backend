from django_filters.rest_framework import FilterSet
import django_filters
from course.models import Course

class CourseFilter(django_filters.FilterSet):
    class Meta:
        model = Course
        fields ={
            'id' : ['exact'],
            'price' : ['gt','lt']
        }


