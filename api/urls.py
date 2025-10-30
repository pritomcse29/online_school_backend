from django.urls import path,include
from rest_framework.routers import DefaultRouter
from course.views import courseImageView,subjectImageView
from course import views
from order.views import admin_update_order_status,admin_dashboard_view,payment_cancel,payment_fail,payment_success,initiate_payment,admin_update_order_status,add_course_view,student_dashboard_view,teacher_dashboard_view,cancel_order,Enrollment_Delete_view,count_view_set,adminTeacherView,Enrollment_view,Enrollment_view_create,Order_view,order_view_set,admin_view_set,reviewCreate
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
    path('admin/dashboard/', admin_dashboard_view, name='admin-dashboard'),
    path('admin-teacher/',adminTeacherView,name="admin-teacher"),
    path('count-view/',count_view_set,name="count-view"),
    # path('enrollment-item/<int:pk>/delete/', Enrollment_Delete_view, name='enrollment-item-delete'),
    path('enrollment/item/<int:pk>/delete/', Enrollment_Delete_view),
    path('order/<uuid:order_id>/cancel/', cancel_order, name='cancel_order'),
    path('dashboard/teacher/', teacher_dashboard_view),
    path('dashboard/student/', student_dashboard_view),
    path('course/add/', add_course_view),
    path('order/<uuid:order_id>/admin-update/', admin_update_order_status),
    path("payment/initiate/",initiate_payment,name="initiate-payment"),
    path("payment/success/",payment_success,name="payment-success"),
    path("payment/fail/",payment_fail,name="payment-fail"),
    path("payment/cancel/",payment_cancel,name="payment-cancel"),
    # path('dashboard/adminUpdateStatus/<int:order_id>/', views.admin_update_order_status, name='admin_update_order_status'),
   
    # path('review-create/',review_create,name="review-create")
]