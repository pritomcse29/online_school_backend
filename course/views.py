from course.serializers import CourseSerializer,SubjectSerializer
from course.models import Course,Subject
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from course.permission import IsAdmin,IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,IsTeacherOrAdmins

# from course.permission import isAdmin,IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,isStudent,isTeacher
# Create your views here.

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsTeacherOrAdmins]
    def get_permissions(self):
      if self.action in ['create', 'update', 'partial_update', 'destroy']:
          return [IsTeacherOrAdmins(),IsOwnerOrReadOnly()]
      return [IsAuthenticatedOrReadOnly()]
    # def get_queryset(self):
    #     user = self.request.user
    #     if user.role == 'teacher':
    #         return Course.objects.filter(owner=user)
    #     elif user.role == 'admin':
    #         return Course.objects.all()
    # def get_permissions(self):
    #     if self.action in ['create','update','partial_update','destroy']:
    #         return [IsAdmin(),IsOwnerOrReadOnly()]
    #     return [IsAuthenticatedOrReadOnly()]
        

 
    
class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAdmin]

    def get_permissions(self):
        if self.action in ['create','update','partial_update','destroy']:
            return [IsAdmin()]
        return [IsAuthenticatedOrReadOnly()]



