from course.models import Course,Subject,CourseImage,SubjectImage
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class courseImageSerializer(serializers.ModelSerializer):
    image =  serializers.ImageField()
    class Meta:
        model = CourseImage
        fields =['id','image']
class CourseSerializer(serializers.ModelSerializer):
    courseImage = courseImageSerializer(many=True, read_only=True)
    class Meta:
        model = Course
        fields =['id','name','description','price','available_seat','created_at','updated_at','duration','subject','owner','courseImage']
        read_only = ['created_at']

        def perform_create(self, serializer):
            serializer.save(owner=self.request.user)

        def __str__(self):
            return f"self.name"
class SubjectImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = SubjectImage
        fields =['id','image']
        
class SubjectSerializer(serializers.ModelSerializer):
    subjectImage = SubjectImageSerializer(many=True,read_only=True)

    class Meta:
        model = Subject
        fields = ['id','title','slug','subjectImage']

        def __str__(self):
            return f"self.title"


