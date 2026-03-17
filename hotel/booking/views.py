from rest_framework import viewsets, permissions, generics
from django_filters import rest_framework as filters
from .models import Booking, Room
from .serializers import RoomSerializer, UserSerializer, BookingSerializer
from django.contrib.auth.models import User


class RoomFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price_per_night", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price_per_night", lookup_expr='lte')
    
    
    start_date = filters.DateFilter(method='filter_availability')
    end_date = filters.DateFilter(method='filter_availability')

    class Meta:
        model = Room
        fields = ['capacity','min_price','max_price']


    def filter_availability(self, queryset, name, value):
        # Logic: Exclude rooms that have bookings overlapping with the requested range
        data = self.request.query_params
        start = data.get('start_date')
        end = data.get('end_date')

        if start and end:
            # Find rooms that ARE booked during this time
            booked_rooms = Booking.objects.filter(
                start_date__lt=end,
                end_date__gt=start
            ).values_list('room_id', flat=True)
            
            # Return rooms NOT in that list
            return queryset.exclude(id__in=booked_rooms)
        return queryset

from django.db.models import QuerySet

class RoomViewSet(viewsets.ReadOnlyModelViewSet):
    queryset: QuerySet[Room] = Room.objects.all().order_by('price_per_night')
    serializer_class = RoomSerializer


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Superusers see everything, regular users see only their own bookings
        if self.request.user.is_superuser:
            return Booking.objects.all()
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # The serializer now handles the user via the context or explicit assignment
        serializer.save(user=self.request.user)



class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can sign up