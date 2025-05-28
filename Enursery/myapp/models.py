
from django.db import models
from django.contrib.auth.models import User

# ----------------- CATEGORY MODEL -----------------
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# ----------------- PRODUCT MODEL -----------------
class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)

    def __str__(self):
        return self.name


# ----------------- CART & CART ITEM MODELS -----------------
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Multiple carts possible

    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


# ----------------- CONTACT FORM MODEL -----------------
class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name


# ----------------- USER PROFILE MODEL -----------------
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)  # Ensure this field exists
    phone = models.CharField(max_length=15, blank=True, null=True, default="Not Provided")
    billing_address = models.TextField(blank=True, null=True)
    shipping_address = models.TextField(blank=True, null=True,default="Not Provided")

    def __str__(self):
        return self.user.username


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)  # ✅ Create profile for new users

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


# ----------------- ORDER MODEL -----------------
class Order(models.Model):
    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')

    def __str__(self):
        return f"Order {self.id} - {self.user.username} - {self.status}"


# ----------------- WISHLIST MODEL -----------------
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)  # Add this field with default value

    class Meta:
        unique_together = ('user', 'product')  # Prevent duplicate wishlist items

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"




# from django.db import models
# from django.contrib.auth.models import User 

# from django.db import models

# from django.db import models

# class Category(models.Model):
#     name = models.CharField(max_length=100, unique=True)

#     def __str__(self):
#         return self.name

# class Product(models.Model):
#     name = models.CharField(max_length=200)
#     category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     stock = models.PositiveIntegerField(default=0)  # Ensure 'stock' is correctly defined
#     image = models.ImageField(upload_to='product_images/', null=True, blank=True)

#     def __str__(self):
#         return self.name

    

# class Cart(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"Cart of {self.user.username}"

# class CartItem(models.Model):
#     cart = models.ForeignKey("Cart", on_delete=models.CASCADE, related_name="items")
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Ensure this is correct
#     quantity = models.PositiveIntegerField(default=1)

#     def __str__(self):
#         return f"{self.quantity} x {self.product.name}"



# class Contact(models.Model):
#     name = models.CharField(max_length=255)
#     email = models.EmailField()
#     message = models.TextField()

#     def __str__(self):
#         return self.name


# from django.db import models
# from django.contrib.auth.models import User

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     phone = models.CharField(max_length=15)
#     billing_address = models.TextField()
#     shipping_address = models.TextField()

# class Product(models.Model):
#     name = models.CharField(max_length=255)
#     price = models.DecimalField(max_digits=10, decimal_places=2)

# class Order(models.Model):
#     STATUS_CHOICES = [
#         ('processing', 'Processing'),
#         ('shipped', 'Shipped'),
#         ('delivered', 'Delivered'),
#     ]
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')

# class Wishlist(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)


# from django.db import models
# from django.contrib.auth.models import User

# class Category(models.Model):
#     name = models.CharField(max_length=255, unique=True)
#     description = models.TextField(blank=True, null=True) 
#     class Meta:
#         verbose_name_plural = "Categories"
#     def __str__(self):
#         return self.name

# class Product(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     id = models.BigAutoField(primary_key=True)  # This must be an AutoField
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
#     # is_active = models.BooleanField(default=True)
#     stock = models.IntegerField(default=0) 
#     # created_at = models.DateTimeField(auto_now_add=True)  # This should be for timestamps

#     def __str__(self):
#         return self.name

# class Cart(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    
#     def __str__(self):
#         return f"Cart of {self.user.username}"

# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)

#     def __str__(self):
#         return f"{self.quantity} x {self.product.name}"

# class Contact(models.Model):
#     name = models.CharField(max_length=255)
#     email = models.EmailField()
#     message = models.TextField()

#     def __str__(self):
#         return self.name

# # from django.db import models

# # class Category(models.Model):
# #     name = models.CharField(max_length=100, unique=True)
# #     description = models.TextField(blank=True, null=True)
# #     image = models.ImageField(upload_to='category_images/', blank=True, null=True)

# #     def __str__(self):
# #         return self.name

# # class Product(models.Model):
# #     name = models.CharField(max_length=100)    
# #     description = models.TextField()
# #     price = models.DecimalField(max_digits=10, decimal_places=2)
# #     stock = models.PositiveIntegerField(default=0)
# #     image = models.ImageField(upload_to='product_images/', blank=True, null=True)
# #     category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
# #     is_active = models.BooleanField(default=True)   # Only show active products

# #     def __str__(self):
# #         return self.name


# # from django.contrib.auth.models import User

# # class Cart(models.Model):
# #     user = models.ForeignKey(User, on_delete=models.CASCADE)
# #     product = models.ForeignKey(Product, on_delete=models.CASCADE)
# #     quantity = models.PositiveIntegerField(default=1)
# #     added_at = models.DateTimeField(auto_now_add=True)
    

# #     def __str__(self):
# #         return f"{self.user.username} - {self.product.name}"
    

# # class Contact(models.Model):
# #     name = models.CharField(max_length=100)
# #     email = models.EmailField()
# #     message = models.TextField()

# #     def __str__(self):
# #         return self.name
    

# #     def __str__(self):
# #         return self.name

# # from django.contrib.auth.models import User

# # class CartItem(models.Model):
# #     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
# #     product = models.ForeignKey(Product, on_delete=models.CASCADE)
# #     quantity = models.PositiveIntegerField(default=1)
# #     added_at = models.DateTimeField(auto_now_add=True)







       