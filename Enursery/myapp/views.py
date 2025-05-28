from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Product, Category, Cart, CartItem
from .forms import ContactForm

# --------------------- Home & Authentication ---------------------

def home(request):
    # products = Product.objects.all()  # Ensure this returns actual products
    categories = Category.objects.all()
    return render(request, 'home.html', {"categories": categories, "products": products})

def aboutUs(request):
    return render(request, 'aboutUs.html')

def contactus(request):
    return render(request, 'contactus.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password!")
            return redirect('signin')
    return render(request, 'signin.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('signup')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        login(request, user)
        messages.success(request, "Sign-up successful!")
        return redirect('home')
    return render(request, 'signup.html')

@login_required
def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('signin')

# --------------------- Product & Category Views ---------------------
from django.template.loader import get_template


def products(request):
    categories = Category.objects.all()  # Get all categories for sidebar
    selected_category_id = request.GET.get('category')  # Get selected category from URL parameters
    
    if selected_category_id:
        products = Product.objects.filter(category_id=selected_category_id)  # Filter products by category
    else:
        products = Product.objects.all()  # Get all products

    return render(request, 'product.html', {'categories': categories, 'products': products})


# def products(request):
#     categories = Category.objects.all()
#     products = Product.objects.all()
#     # products = Product.objects.filter()
#     print(get_template('product.html').template.name)  # Confirm template path

#     print("Categories:", categories)  # Debug categories
#     print("Products:", products)
#     return render(request, 'product.html', {'categories': categories, 'products': products})

def products_by_category(request, category_id):
    categories = Category.objects.all()
    selected_category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=selected_category)
    return render(request, 'product.html', {'categories': categories, 'products': products, 'selected_category': selected_category})



def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    return render(request, 'product_detail.html', {'product': product})


# --------------------- Cart Management ---------------------

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 1})

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


from django.shortcuts import get_object_or_404, redirect
from .models import Cart, CartItem

def remove_from_cart(request, product_id):
    # Ensure the user has a cart
    cart = Cart.objects.filter(user=request.user).first()
    if not cart:
        return redirect('cart')  # Redirect if no cart exists

    # Ensure the cart item exists
    cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
    if not cart_item:
        return redirect('cart')  # Redirect if no cart item found

    # Decrease quantity or remove item
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')


# @login_required
# def remove_from_cart(request, product_id):
#     cart = Cart.objects.filter(user=request.user).first()
#     if cart:
#         cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
#         if cart_item:
#             cart_item.delete()
#     return redirect('cart')


@login_required
def cart_view(request):
    # Retrieve the cart for the logged-in user
    cart = Cart.objects.filter(user=request.user).first()
    
    # If no cart exists, return an empty cart
    if not cart:
        return render(request, 'cart.html', {'cart_items': [], 'total_price': 0})

    # Access related cart items using the default related name
    cart_items = cart.items.all()  # or use cart.items.all() if you set related_name="items"
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()
    
    if not cart or not cart.items.exists():
        messages.error(request, "Your cart is empty!")
        return redirect('cart')

    cart_items = cart.items.all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })


from django.shortcuts import redirect

def place_order(request):
    if request.method == "POST":
        # Process the order logic here
        return redirect('home')  # Redirect to home after order completion
    return redirect('checkout')


# @login_required
# def checkout(request, product_id=None):
#     if product_id:
#         product = get_object_or_404(Product, id=product_id)
#         return render(request, 'checkout.html', {'product': product})

#     cart = Cart.objects.filter(user=request.user).first()
#     cart_items = cart.items.all()
#     total_price = sum(item.product.price * item.quantity for item in cart_items)

    
#     return render(request, 'checkout.html', {'cart_items': cart_items, 'total': total_price})

# --------------------- Contact Form ---------------------

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'thanks.html')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


# Account pages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order, Wishlist, Profile, Product

@login_required
def dashboard(request):
    recent_orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    wishlist_items = Wishlist.objects.filter(user=request.user)
    recommended_plants = Product.objects.filter(category__in=[order.product.category for order in recent_orders])[:4]
    
    return render(request, 'dashboard.html', {
        'recent_orders': recent_orders,
        'wishlist_items': wishlist_items,
        'recommended_plants': recommended_plants,
    })

@login_required
def personal_info(request):
    profile = get_object_or_404(Profile, user=request.user)
    
    if request.method == "POST":
        profile.name = request.POST.get('name')
        profile.email = request.POST.get('email')
        profile.phone = request.POST.get('phone')
        profile.billing_address = request.POST.get('billing_address')
        profile.shipping_address = request.POST.get('shipping_address')
        profile.save()
        return redirect('personal_info')

    return render(request, 'personal_info.html', {'profile': profile})

@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders.html', {'orders': orders})

@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)  # Avoid duplicates
    return redirect('wishlist')  # Redirect to Wishlist Page

# Remove from Wishlist
@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    return redirect('wishlist')

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile

@login_required
def account_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)  # ✅ Ensures profile exists
    return render(request, 'account/account.html', {'profile': profile})





# from django.shortcuts import render
# from .forms import ContactForm 
# from .models import Product, Cart
# from django.shortcuts import render, get_object_or_404
# from .models import Product
# from django.shortcuts import render


# def home(request):
#     return render(request, 'home.html')

# def aboutUs(request):
#     return render(request, 'aboutUs.html')

# def contactus(request):
#     return render(request, 'contactus.html')

# def signin(request):
#     return render(request, 'signin.html')

# def signup(request):
#     return render(request, 'signup.html')






# from django.contrib.auth.forms import UserCreationForm
# from django.shortcuts import render, redirect

# from django.contrib.auth.models import User
# from django.contrib.auth import login
# from django.contrib import messages

# def signup(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         confirm_password = request.POST.get('confirm_password')

#         if password != confirm_password:
#             messages.error(request, "Passwords do not match!")
#             return redirect('signup')

#         # Check if the username or email already exists
#         if User.objects.filter(username=username).exists():
#             messages.error(request, "Username already exists!")
#             return redirect('signup')
#         if User.objects.filter(email=email).exists():
#             messages.error(request, "Email already registered!")
#             return redirect('signup')

#         # Create a new user
#         user = User.objects.create_user(username=username, email=email, password=password)
#         user.save()

#         login(request, user)  # Log the user in after signup
#         messages.success(request, "Sign-up successful!")
#         return redirect('home')  # Redirect to the homepage or any other page
#     return render(request, 'signup.html')  # Render your existing sign-up form

# from django.contrib.auth import logout

# def signout(request):
#     logout(request)
#     messages.success(request, "Logged out successfully!")
#     return redirect('signin')  # Redirect to the sign-in page
# from django.contrib.auth.decorators import login_required

# @login_required
# def dashboard(request):
#     return render(request, 'dashboard.html')

# from django.contrib.auth import authenticate, login

# def signin(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             messages.success(request, "Logged in successfully!")
#             return redirect('home')  # Redirect to the homepage or another page
#         else:
#             messages.error(request, "Invalid username or password!")
#             return redirect('signin')
#     return render(request, 'signin.html')  # Render your existing sign-in form

# from django.shortcuts import render

# def home(request):
#     if request.user.is_authenticated:
#         return render(request, 'home.html', {'username': request.user.username})
#     else:
#         return render(request, 'home.html', {'message': 'You are not signed in!'})
    
# def product_list(request):

#     products = Product.objects.filter(is_active=True)
#     products = Product.objects.all()
#     return render(request, 'product.html', {'products': products})


# from django.shortcuts import render, get_object_or_404
# from .models import Product, Category

# def products(request):
#     categories = Category.objects.all()
#     products = Product.objects.all()
#     return render(request, 'product.html', {'categories': categories, 'products': products})

# def products_by_category(request, category_id):
#     categories = Category.objects.all()
#     selected_category = get_object_or_404(Category, id=category_id)
#     products = selected_category.products.all()
#     return render(request, 'product.html', {'categories': categories, 'products': products})



# from django.shortcuts import get_object_or_404, redirect
# from .models import Product, Cart

# def add_to_cart(request, product_id):
#     if request.user.is_authenticated:
#         # Retrieve the product
#         product = get_object_or_404(Product, id=product_id)

#         # Check if the product already exists in the cart
#         cart_item, created = Cart.objects.get_or_create(
#             product=product,
#             user=request.user,  # Associate the cart item with the logged-in user
#             defaults={'quantity': 1}  # Set initial quantity to 1 if creating a new item
#         )

#         # If the item already exists, increase the quantity
#         if not created:
#             cart_item.quantity += 1
#             cart_item.save()

#         # Redirect to the cart page
#         return redirect('cart')  # Replace 'cart' with the name of your cart page URL
#     else:
#         # Redirect to the login page if the user is not authenticated
#         return redirect('signin')  # Replace 'signin' with the name of your login page URL
#  # Redirect to login if not authenticated


# def cart(request):
#     if request.user.is_authenticated:
#         cart_items = Cart.objects.filter(user=request.user)
#         total = sum(item.product.price * item.quantity for item in cart_items)
#         return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})
#     else:
#         return redirect('signin')


# def checkout(request, product_id):
#     product = Product.objects.filter(id=product_id).first()
#     if not product:
#         product = get_object_or_404( id=product_id)
    
#     return render(request, 'checkout.html', {'product': product})



# from django.shortcuts import redirect
# from django.http import HttpResponse

# from django.shortcuts import redirect, get_object_or_404
# from .models import CartItem

# def remove_from_cart(request, product_id):
#     if request.method == "POST":
#         cart_item = get_object_or_404(CartItem, product_id=product_id, user=request.user)
#         cart_item.delete()  # Remove the item from the database
#         return redirect('cart')
#     else:
#         return HttpResponse("Invalid request method.", status=405)




# def contact(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return render(request, 'thanks.html')
#     else:
#         form = ContactForm()
#     return render(request, 'contact.html', {'form': form})

# from django.shortcuts import render, get_object_or_404


# from django.shortcuts import get_object_or_404, render

# from django.shortcuts import redirect, get_object_or_404
# from .models import  Cart

# def buy_now(request):
#     plant = get_object_or_404( )
#     # Redirect to checkout page or handle immediate purchase logic
#     return redirect('checkout')  # Replace 'checkout' with your checkout view name




# from django.shortcuts import get_object_or_404, redirect
# from .models import Cart, CartItem, Product


# def view_cart(request):
#     if request.user.is_authenticated:
#         cart = Cart.objects.filter(user=request.user).first()
#         if not cart:
#             items = []
#         else:
#             items = cart.items.all()
#         return render(request, 'cart.html', {'items': items})
#     else:
#         return redirect('login')
