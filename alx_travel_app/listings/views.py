from django.shortcuts import render
from rest_framework.response import Response

from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer
from .tasks import send_bookingSerializer


class ListingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for hangling CRUD operations for listing model
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for hangling CRUD operations for Booking model.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    
    def create(self, request, **args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Booking instance from the serializer data
        booking = serializer.instance
        
         # Trigger the email task to be sent asynchronously
        send_booking_confirmation_email.delay(
            booking_id=booking.id,
            user_email=booking.user.email,
            listing_title=booking.listing.title
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
