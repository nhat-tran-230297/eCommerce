from django.urls import path

from . import views

app_name = 'payment'

urlpatterns = [
    path('', views.payment_detail, name='payment_detail'),
    path('payment-complete/', views.payment_complete, name='payment_complete'),
    path('webhook/', views.stripe_webhook),
]