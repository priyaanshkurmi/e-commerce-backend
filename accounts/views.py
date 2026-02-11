from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from orders.models import Order


@login_required
def dashboard(request):
    """User dashboard showing orders and profile summary"""
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')
    
    context = {
        'user': user,
        'orders': orders,
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
    
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        
        return redirect('profile')
    
    return render(request, 'accounts/profile.html', {
        'user': user
    })
