from django.db import models
from django.contrib.auth.models import User
from django_google_maps import fields as map_fields
from django.db.models.signals import post_save
from django.dispatch import receiver

# ==========================
# 1. CHOICE TUPLES
# ==========================
STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Scheduled', 'Scheduled'),
    ('In Progress', 'In Progress'),
    ('Packed', 'Packed'),
    ('Shipped', 'Shipped'),
    ('Ready For Pickup', 'Ready For Pickup'),
    ('Delivered', 'Delivered'),
)

# ==========================
# 2. MODELS
# ==========================
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1)

    customer_name = models.CharField('Name', max_length=100, null=True, blank=True)
    customer_email = models.EmailField('Email', max_length=100, null=True, blank=True)
    customer_phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(default="", blank=True) 
    city = models.CharField(max_length=100, default="", blank=True)

    transaction_id = models.CharField(max_length=100, null=True, blank=True)

    status = models.CharField(
        'Order Status',
        max_length=50, 
        choices=STATUS_CHOICES, 
        default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        product_name = self.product.name if self.product else "Unknown Item"
        return f"Order #{self.id} - {product_name} (Qty: {self.quantity})"

class Map(models.Model):
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)

    def __str__(self):
        return self.address

class Feedback(models.Model):
    customer_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    rating = models.IntegerField(default=5, help_text="Rating out of 5")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.rating} Stars"
    
# ==========================
# 3. USER PROFILE (Auto-linked)
# ==========================
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

# === AUTOMATIC PROFILE CREATION (Signals) ===
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()
    else:
        UserProfile.objects.create(user=instance)