from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# class Room(models.Model):
#     number = models.CharField()
#     price_per_night = models.DecimalField()
#     capacity = models.PositiveIntegerField()
    

#     def __str__(self):
#         return f"Room {self.number} - {self.capacity} seats"



class Room(models.Model):
    # max_length is required for CharField
    number = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name="Room Number/Name"
    )
    
    # DecimalFields require both max_digits and decimal_places
    # max_digits=10 and decimal_places=2 allows up to 99,999,999.99
    price_per_night = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Price per Night"
    )
    
    capacity = models.PositiveIntegerField(verbose_name="Number of Seats")

    def __str__(self):
        return f"Room {self.number}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.room.number}"

    def clean(self):
        # Logic for Django Admin validation
        if self.start_date and self.end_date:
            if self.start_date >= self.end_date:
                raise ValidationError("End date must be after start date.")
            
            overlap = Booking.objects.filter(
                room=self.room,
                start_date__lt=self.end_date,
                end_date__gt=self.start_date
            ).exclude(pk=self.pk).exists()
            
            if overlap:
                raise ValidationError("Room is already booked for these dates.")

    def save(self, *args, **kwargs):
        self.full_clean() # This ensures clean() is called before saving
        super().save(*args, **kwargs)