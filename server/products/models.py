from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    # Explicitly set related_name to avoid clashes
    # groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    
    def __str__(self):
        return self.username



class Item(models.Model):
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Beverage', 'Beverage'),
        ('Personal Care', 'Personal Care'),
        ('Household', 'Household'),
        # Add more categories as needed
    ]

    UNIT_CHOICES = [
        ('kgs', 'Kilograms'),
        ('grams', 'Grams'),
        ('litres', 'Litres'),
        ('millilitres', 'Millilitres'),
        ('pieces', 'Pieces'),
        ('meters', 'Meters'),
        ('inches', 'Inches'),
        # Add more unit choices as needed
    ]

    product_name = models.CharField(max_length=255)
    barcode = models.CharField(max_length=100, blank=True, null=True)
    expiration_date = models.DateField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='Food')
    quantity = models.DecimalField(max_digits=30, decimal_places=2)
    quantity_unit = models.CharField(max_length=30, choices=UNIT_CHOICES, default='grams')
    priority = models.IntegerField(default=0)
      # New image field
    image = models.ImageField(upload_to='item_images/', null=True, blank=True)

    # Foreign key relationship with CustomUser
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='items', null=True, blank=True)

    def __str__(self):
        return self.product_name

