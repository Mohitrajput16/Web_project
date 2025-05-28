from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('aboutUs/', views.aboutUs, name='aboutUs'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('contactus/', views.contactus, name='contactus'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('place_order/', views.place_order, name='place_order'),
    
    path('products/', views.products, name='products'),  # FIXED: 'product/' → 'products/'
    path('products/category/<int:category_id>/', views.products_by_category, name='products_by_category'),  

    path('signout/', views.signout, name='signout'),
    path('cart/', views.cart_view, name='cart'),
    # path('checkout/<int:product_id>/', views.checkout, name='checkout'),
    path('checkout/', views.checkout, name='checkout'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Only keep **one** add-to-cart URL (choose the correct one based on your logic)
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),


    path('dashboard/', views.dashboard, name='dashboard'),
    path('personal-info/', views.personal_info, name='personal_info'),
    path('orders/', views.orders, name='orders'),
    path('wishlist/',views.wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
]




# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
