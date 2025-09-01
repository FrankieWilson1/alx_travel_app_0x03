"""
Serializers for the Listings, Bookings, and Review app.

This module defines Django REST Framework serializers to convert
model instances into JSON (or other content types) and vice-versa,
facilitating API interactions.
"""

from rest_framework import serializers
from .models import Listing, Booking

class ListingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Listing model.
    Converts Listing model instances to JSON and handles validation
    for incoming data.
    """
    class Meta:
        model = Listing
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Booking model.
    Converts Booking model instances to JSON and handles validation for
    incoming data
    """
    list_title = serializers.ReadOnlyField(source='listing.title')
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Booking
        fields = (
            'id', 'list_title', 'username', 'start_date', 'end_date',
            'total_price', 'is_confirmed', 'created_at'
        )
