from django.urls import path,include
from rest_framework.routers import DefaultRouter
from course import views
from order.views import Enrollment_view,Enrollment_view_create,Order_view,order_view_set,admin_view_set
router = DefaultRouter()

router.register(r'courses', views.CourseViewSet, basename='courses')
router.register(r'subjects', views.SubjectViewSet, basename='subjects')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('enrollment/', Enrollment_view_create, name='enrollment'),
    path('cart/', Enrollment_view, name='view-cart'),
    path('create-order/',Order_view, name='create-order'),
    path('order-view/',order_view_set,name="order-view-set"),
    path('admin-view-set/',admin_view_set,name='admin-view-set')
]