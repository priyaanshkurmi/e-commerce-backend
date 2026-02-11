from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('orders/', views.order_history, name='order_history'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('profile/', views.profile, name='profile'),
    path('address/', views.manage_address, name='manage_address'),
]
