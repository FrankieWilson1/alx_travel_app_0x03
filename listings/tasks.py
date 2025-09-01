from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_booking_confirmation_email(booking_id, user_email, listing_title):
    """
    Sends a booking confirmation email to the user.
    """
    subject = f"Booking Confirmation for {listing_title}"
    message = f"Hello,\n\nYour booking for {listing_title} has been confirmed. Thank you for using our service!"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        print(f"Successfully sent booking confirmation email to {user_email}")
    except Exception as e:
        print(f"Failed to send email to {user_email}: {e}")
