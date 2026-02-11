from django.urls import path
from . import views

urlpatterns = [
    path("pay/<int:order_id>/", views.start_payment, name="start_payment"),
    path("verify/", views.verify_payment, name="verify_payment"),
    path("success/", views.payment_success, name="payment_success"),
]