from django.contrib import admin
from .models import Listing, Booking, Review


class ListingAdmin(admin.ModelAdmin):
    """
    Customizes the display and functionlity of the Listing
    models in the Django admin interface.
    """
    list_display = (
        'id', 'title', 'is_published', 'price', 'list_date', 'city', 'state'
    )
    list_display_links = ('id', 'title')
    list_filter = ('city', 'state')
    search_fields = ('title', 'description', 'address', 'city', 'state',
                     'zipcode', 'price')
    list_per_page = 25


class BookingAdmin(admin.ModelAdmin):
    """
    Customizes the display and functionality of the Booking model
    in the Django admin interface.
    """
    list_display = (
        'id', 'listing', 'user', 'start_date', 'total_price', 'is_confirmed', 'created_at'
    )
    list_display_links = ('id', 'listing')
    listing_filter = ('listing', 'user', 'is_confirmed')
    search_fields = ('listing__title', 'user__username')
    list_per_page = 25


class ReviewAdmin(admin.ModelAdmin):
    """
    Customizes the display and functionality of the Review model
    in the Django admin interface.
    """
    list_display = (
        'id', 'listing', 'user', 'rating', 'created_at'
    )
    list_display_links  = ('id', 'listing')
    list_filter = ('listing', 'user', 'rating')
    search_fields = ('listing__title', 'user__username', 'comment')
    list_per_page = 25

admin.site.register(Listing, ListingAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Review, ReviewAdmin)
