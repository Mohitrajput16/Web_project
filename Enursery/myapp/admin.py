from django.contrib import admin
from .models import Product, Category, Cart, CartItem, Wishlist, Profile

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_category', 'price', 'stock')  # Fix 'stock' issue
    list_filter = ('category',)  # Ensure 'category' is a valid field

    def get_category(self, obj):
        return obj.category.name if obj.category else "-"
    get_category.short_description = 'Category'  # Display name in Admin Panel

admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Wishlist)
admin.site.register(Profile)


# # admin.py
# from django.contrib import admin
# from .models import Category, Product

# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'description')

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('name', 'category', 'price', 'stock')
#     list_filter = ('category',)

# from django.contrib import admin
# from .models import Product, Category, Cart, CartItem, Wishlist, Profile

# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'category', 'price', 'stock')  # Ensure 'category' and 'stock' exist in Product
#     list_filter = ('category',)  # Ensure 'category' is a valid field

# # admin.site.register(Product)
# # admin.site.register(Category)
# admin.site.register(Cart)
# admin.site.register(CartItem)
# admin.site.register(Wishlist)
# admin.site.register(Profile)
