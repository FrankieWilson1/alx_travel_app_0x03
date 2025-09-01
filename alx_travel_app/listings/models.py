"""
Django models for managing travel listing within the ALX Travel App.

This module defines the Listing, Booking, and Review models, which
represents travel properties, user bookings for these properties,
and user reviews of their experience.
"""


from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Listing(models.Model):
    """
    Represents a single travel listing, such as a house, apartment,
    or other property.

    Attributes:
        title (str): The main title or name of the listing.
        address (str): The street address of the property.
        city (str): The city where the property is located.
        state (str): The state where the property is located.
        zipcode (str): The postal code of the property.
        description (str): A detailed description of the property.
        price (int): The price of the listing.
        bedrooms (int): The number of bedrooms in the property.
        garage (bool): Indicates if the property has a garage.
        lot_size (float): The size of the property's lot.
        photo_main (ImageField): The primary photo of the property.
        photo_1 to photo_6 (ImageField): Additional photos of the property.
        is_published (bool): Indicates if the listing is publicly visible.
        list_date (datetime): The date and time when the listing was added.
    """

    # Basic_Info.
    title = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    description = models.TextField(blank=True)    # Description is optional

    # Property Details
    price = models.IntegerField()   # Stores prices as integer.
    bedrooms = models.IntegerField()
    bathrooms = models.DecimalField(
        max_digits=2,
        decimal_places=1,
    )
    garage = models.BooleanField(default=False)
    sqft = models.IntegerField()
    lot_size = models.DecimalField(
        max_digits=5, decimal_places=2
    )

    # Images
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/')
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_5 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_6 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)

    # Status & Date
    is_published = models.BooleanField(default=True)
    list_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        """
        Returns a string representation of the Listing.
        """
        return self.title

    class Meta:
        """
        Meta options for the Listing model.
        Defines default ordering and verbose name for the admin interface.
        """
        ordering = ['-list_date']
        verbose_name_plural = 'Listings'


class Booking(models.Model):
    """
    Represents a booking made by a user for a specific listing.
    Attributes:
        listing (ForeignKey): The Listing object being booked.
        user (ForeignKey): The User who made the booking.
        start_date (DateField): The start date of the booking.
        end_date (DateField): The end date of the booking.
        total_price (DecialField): The total calculated price forthe booking.
        is_confirmed (BooleanField): Indicates if the booking has been
        confirmed.
        created_at (DateField): The date and time wen the booking was created.
    """
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Returns a string reprensentation of the Booking."""
        return f"Booking for {self.listing.title} by {self.user.username}"

    class Meta:
        """Meta options for the Booking model"""
        ordering = ['-created_at']
        verbose_name_plural = "Bookings"


class Review(models.Model):
    """
    Represents a review given by a user for a specific listing.

    Attributes:
        listing (ForeignKey): The Listing object being reviewed
        user (ForeignKey): The User who wrote the review
        rating (int): The star rating given by the user (1 to 5)
        comment (str): The text content of the review.
        created_at (DateTimmeField): The date and time when the review
        was created.
    """
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Returns a string representation of the Review"""
        rating = self.rating
        user = self.user.username
        title = self.listing.title
        return f"Review for {title} by {user} - Rating: {rating}"

    class Meta:
        """Meta options for the Review model"""
        ordering = ['-created_at']
        verbose_name_plural = "Reviews"
