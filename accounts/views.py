from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from orders.models import Order
from .models import Address


@login_required
def dashboard(request):
    """User dashboard showing orders and profile summary"""
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')
    address = Address.objects.filter(user=user).first()
    
    context = {
        'user': user,
        'orders': orders,
        'address': address,
        'total_orders': orders.count(),
        'paid_orders': orders.filter(status='paid').count(),
        'pending_orders': orders.filter(status='pending').count(),
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required
def order_history(request):
    """Display user's order history"""
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')
    
    return render(request, 'accounts/order_history.html', {
        'orders': orders
    })


@login_required
def order_detail(request, order_id):
    """Display details of a specific order"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    return render(request, 'accounts/order_detail.html', {
        'order': order
    })


@login_required
def profile(request):
    """User profile page"""
    user = request.user
    address = Address.objects.filter(user=user).first()
    
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        
        return redirect('profile')
    
    return render(request, 'accounts/profile.html', {
        'user': user,
        'address': address
    })


@login_required
def manage_address(request):
    """Create or edit user address"""
    user = request.user
    address = Address.objects.filter(user=user).first()
    
    if request.method == 'POST':
        if address:
            # Update existing address
            address.full_name = request.POST.get('full_name')
            address.phone = request.POST.get('phone')
            address.address_line_1 = request.POST.get('address_line_1')
            address.address_line_2 = request.POST.get('address_line_2')
            address.city = request.POST.get('city')
            address.state = request.POST.get('state')
            address.postal_code = request.POST.get('postal_code')
            address.country = request.POST.get('country', 'India')
            address.save()
        else:
            # Create new address
            address = Address.objects.create(
                user=user,
                full_name=request.POST.get('full_name'),
                phone=request.POST.get('phone'),
                address_line_1=request.POST.get('address_line_1'),
                address_line_2=request.POST.get('address_line_2'),
                city=request.POST.get('city'),
                state=request.POST.get('state'),
                postal_code=request.POST.get('postal_code'),
                country=request.POST.get('country', 'India')
            )
        
        return redirect('profile')
    
    return render(request, 'accounts/manage_address.html', {
        'address': address
    })
