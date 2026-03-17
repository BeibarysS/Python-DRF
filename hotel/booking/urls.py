# booking/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, BookingViewSet, UserCreateView
from rest_framework.authtoken import views as auth_views

router = DefaultRouter()
router.register(r'rooms', RoomViewSet, basename='room')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('', include(router.urls)), # This includes all ViewSet routes
    path('register/', UserCreateView.as_view(), name='register'),
    path('login/', auth_views.obtain_auth_token, name='login'),
]