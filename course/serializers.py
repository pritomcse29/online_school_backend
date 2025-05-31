from course.models import Course,Subject
from rest_framework import serializers

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields =['id','name','description','price','available_seat','created_at','updated_at','duration','subject','owner']
        read_only = ['created_at']

        def perform_create(self, serializer):
            serializer.save(owner=self.request.user)

        def __str__(self):
            return f"self.name"
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id','title','slug']

        def __str__(self):
            return f"self.title"