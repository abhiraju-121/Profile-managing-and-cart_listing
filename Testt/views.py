from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login ,logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . models import Product,Purchase,Cart,CartItem,Order,OrderItem
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from decimal import Decimal


# Create your views here.

def home_index(request):
    return render(request,'home_index.html')


def home(request):
    return render(request,'home.html')

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('register')

        if password != password1:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
        user.save()
        messages.success(request, "Registration successful! Please log in.")
        return redirect('login')

    return render(request, 'register.html')

def login(request):
    if request.method == "POST":
        username = request.POST.get('username') 
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password!")
            return redirect('login')
    return render(request, 'login.html')


def logout(request):
    auth_logout(request)
    messages.success(request,"Logout success")
    return redirect('home_index')


@login_required(login_url='login')
def profile(request):
    return render(request, 'profile.html')

@login_required(login_url='login')
def update_profile(request):
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('profile')

    return render(request, 'update_profile.html')

@login_required(login_url='login')
def deactivate_account(request):
    if request.method == "POST":
        user = request.user
        user.is_active = False
        user.save()
        messages.success(request, "Your account has deactivated")
        return redirect('home_index')
    return render(request, 'deactivate_account.html')

login_required(login_url='login')
def product(request):
    items=Product.objects.all()
    return render(request,'product.html',{'items':items})

@login_required(login_url='login')
def pro_details(request,pro_id):
    products=get_object_or_404(Product,id=pro_id)
    cart,created=Cart.objects.get_or_create(user=request.user)
    context={'products':products,'cart':cart}
    return render(request,'pro_details.html',context)

@login_required(login_url='login')
def purchase(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        customer_name = request.POST.get('customer_name')
        quantity = int(request.POST.get('quantity', 0))

        if quantity <= 0:
            messages.error(request, "No quantity specified.")
        else:
            with transaction.atomic():
                order = Order.objects.create(
                    user=request.user,
                    customer_name=customer_name,
                    total_price=Decimal(0)  
                )
                price = product.price * Decimal(quantity)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=price
                )
                order.total_price += price 
                order.save()

                messages.success(request, f'Purchase successful! Total: ${price}')
            return redirect('pro_details', pro_id=product.id)

    return render(request, 'purchase.html', {'product': product})

@receiver(post_save, sender=Purchase)
def update_cart_after_purchase(sender, instance, created, **kwargs):
    if created:
        cart, created = Cart.objects.get_or_create(user=instance.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=instance.product)

        if not created:
            cart_item.quantity += instance.quantity
        else:
            cart_item.quantity = instance.quantity
        cart_item.save()

@login_required(login_url='login')
def cart_view(request):
    cart_items = OrderItem.objects.filter(order__user=request.user,)
    total_items = sum(item.quantity for item in cart_items)

    return render(request, 'cart.html', {
        'cart': {
            'items': cart_items,
            'total_items': total_items,
        }
    })

@login_required(login_url='login')
def del_cart_view(request,cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart')

@login_required(login_url='login')
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    grouped_orders = {}
    for order in orders:
        order_date = order.order_date.date()
        if order_date not in grouped_orders:
            grouped_orders[order_date] = []
        items = order.items.all()
        item_count = items.count()

        grouped_orders[order_date].append({
            'order_id': order.id,
            'customer_name': order.customer_name,
            'item_count': item_count,
            'total_price': order.total_price,
            'items': items,
        })

    return render(request, 'order_history.html', {
        'grouped_orders': grouped_orders
    })

@login_required(login_url='login')
def delete_history(request,order_id ):
    history_item=get_object_or_404(Order,id=order_id,user=request.user )
    history_item.delete()
    return redirect('order_history')