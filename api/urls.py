from django.urls import path,include
from rest_framework.routers import DefaultRouter
from course.views import courseImageView,subjectImageView
from course import views
from order.views import count_view_set,adminTeacherView,Enrollment_view,Enrollment_view_create,Order_view,order_view_set,admin_view_set,reviewCreate
from rest_framework_nested import routers
router = DefaultRouter()

router.register(r'courses', views.CourseViewSet, basename='courses')
router.register(r'subjects', views.SubjectViewSet, basename='subjects')
router.register('review-create',reviewCreate,basename='review-create')

course_router = routers.NestedDefaultRouter(router,'courses',lookup ='course' )
course_router.register('images',courseImageView, basename='course-images')

subject_router = routers.NestedDefaultRouter(router,'subjects',lookup ='subject' )
subject_router.register('images',subjectImageView, basename='subject-images')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('', include(course_router.urls)),  # Nested router paths for course images
    path('', include(subject_router.urls)),
    path('enrollment/', Enrollment_view_create, name='enrollment'),
    path('cart/', Enrollment_view, name='view-cart'),
    path('create-order/',Order_view, name='create-order'),
    path('order-view/',order_view_set,name="order-view-set"),
    path('admin-view-set/',admin_view_set,name='admin-view-set'),
    path('admin-teacher/',adminTeacherView,name="admin-teacher"),
    path('count-view/',count_view_set,name=" count-view"),
   
    # path('review-create/',review_create,name="review-create")
]