# hotel/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # This "prefixes" all your booking URLs with 'api/'
    path('api/', include('booking.urls')), 
]