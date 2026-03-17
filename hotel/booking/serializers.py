from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Booking, Room

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)

    class Meta:
        model = User
        fields = ['id', 'username','password','email']
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room 
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, 
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Booking
        fields = ['id', 'room', 'start_date', 'end_date', 'user']
    
    # def validate(self, attrs):
    #     if attrs['start_date'] > attrs['end_date']:
    #         raise serializers.ValidationError("End Date must be after start date")
        
    #     overlapping_booking = Booking.objects.filter(
    #         room = attrs['room'],
    #         start_date__lt = attrs['end_date'],
    #         end_date__lt = attrs['start_date']
    #     ).exists()

    #     if overlapping_booking:
    #         raise serializers.ValidationError("This room is already booked for these dates")
    #     return attrs
    
    def validate(self, attrs):
        room = attrs.get('room')
        start = attrs.get('start_date')
        end = attrs.get('end_date')

        # 1. Basic sanity check
        if start >= end:
            raise serializers.ValidationError("End date must be after start date.")

        # 2. Check for overlaps
        # We look for bookings for the SAME room where dates overlap
        overlapping_bookings = Booking.objects.filter(
            room=room,
            start_date__lt=end,  # Existing starts before new ends
            end_date__gt=start    # Existing ends after new starts
        )

        # If we are UPDATING an existing booking, don't count itself as an overlap
        if self.instance:
            overlapping_bookings = overlapping_bookings.exclude(pk=self.instance.pk)

        if overlapping_bookings.exists():
            raise serializers.ValidationError(
                "This room is already booked for the selected dates."
            )

        return attrs

    def create(self, validated_data):
        # Since 'user' is read_only, we pull it from the context manually
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
        
