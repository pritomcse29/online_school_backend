from course.serializers import CourseSerializer,SubjectSerializer,courseImageSerializer,SubjectImageSerializer
from course.models import Course,Subject,CourseImage,SubjectImage
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from course.permission import IsAdmin,IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,IsTeacherOrAdmins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
 
# from course.permission import isAdmin,IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,isStudent,isTeacher
# Create your views here.

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsTeacherOrAdmins]
    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    filterset_fields = ['name']
    # filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    OrderingFilter = ['price','updated_at']
    pagination_class = PageNumberPagination
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

class courseImageView(viewsets.ModelViewSet):
    # serializer_class = courseImageSerializer
    serializer_class = courseImageSerializer

    def get_queryset(self):
        return CourseImage.objects.filter(course_id=self.kwargs.get('course_pk'))

    def perform_create(self, serializer):
        serializer.save(course_id=self.kwargs.get('course_pk'))
class subjectImageView(viewsets.ModelViewSet):
    serializer_class = SubjectImageSerializer

    def get_queryset(self):
        return SubjectImage.objects.filter(subject_id=self.kwargs.get('subject_pk'))
    
    def perform_create(self, serializer):
        serializer.save(subject_id=self.kwargs.get('subject_pk')) 

    # def get_queryset(self):
    #     # Check if the course exists first
    #     course_id = self.kwargs.get('course')
    #     try:
    #         course = Course.objects.get(id=course_id)
    #     except Course.DoesNotExist:
    #         raise ValueError(f"Course with ID {course_id} does not exist.")
    #     return CourseImage.objects.filter(course=course)

    # def perform_create(self, serializer):
    #     course_id = self.kwargs.get('course')  # Ensure 'course' lookup is correct
    #     if course_id is None:
    #         raise ValueError("Course ID is missing.")
    #     try:
    #         course = Course.objects.get(id=course_id)
    #     except Course.DoesNotExist:
    #         raise ValueError(f"Course with ID {course_id} does not exist.")
    #     serializer.save(course=course)


# class courseImageView(viewsets.ModelViewSet):
#     serializer_class = courseImageSerializer
#     def get_queryset(self):
#         return CourseImage.objects.filter(course_id=self.kwargs.get('course_id'))
#     def perform_create(self, serializer):
#         course_id = self.kwargs.get('course')
#         try:
#             course = Course.objects.get(id=course_id)
#         except Course.DoesNotExist:
#             raise ValueError("Course with ID {} does not exist.".format(course_id))
#         serializer.save(course=course)

    # def perform_create(self,serializer):
    #     course = Course.objects.get(id=self.kwargs.get('course_id'))
    #     # serializer.save(course_id=self.kwargs.get('course_id'))
    #     serializer.save(course=course)
        




