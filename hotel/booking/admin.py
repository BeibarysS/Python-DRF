from django.contrib import admin
from .models import Room, Booking

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'price_per_night', 'capacity')
    search_fields = ('number',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('room', 'user', 'start_date', 'end_date')
    list_filter = ('start_date', 'room')