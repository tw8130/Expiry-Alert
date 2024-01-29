from django.db.models.signals import post_save
from django.dispatch import receiver
from .google_calendar import create_calendar_event
import logging
from .models import Item

@receiver(post_save, sender=Item)
def create_calendar_event_on_save(sender, instance, **kwargs):
     # Triggered whenever a new Item is saved
    try:
        summary = f'Expiry Alert: {instance.product_name}'
        description = f'The product {instance.product_name} is expiring soon.'
        start_datetime = instance.expiration_date.isoformat() + 'Z'
        end_datetime = instance.expiration_date.isoformat() + 'Z'

        create_calendar_event(summary, description, start_datetime, end_datetime)
        
    except Exception as e:
        # Log the error
        print("Error:", str(e))
        logging.error(f"Error creating calendar event: {e}")