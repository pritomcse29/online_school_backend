from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField
class Subject(models.Model):
    title = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)

    def __str__(self):
        return self.title
class SubjectImage(models.Model):
    subject =  models.ForeignKey(Subject,on_delete=models.CASCADE,related_name='subjectImage')
    # image = models.ImageField(upload_to='subject/image')
    image = CloudinaryField('image')
class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100,null=True,blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    available_seat = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    duration = models.DecimalField(max_digits=10,decimal_places=2)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,related_name='courses')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='course_owner',null=True,blank=True)

    def __str__(self):
        return self.name

class CourseImage(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='courseImage')
    image = CloudinaryField('image')
    # image = models.ImageField(upload_to='course/image')

