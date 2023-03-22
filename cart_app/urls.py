from django.urls import path

from . import views
urlpatterns = [
    path('cart_item_api/', views.CartItemAPI.as_view(), name='cart_item_api'),
    path('cart_item_api/<int:id>/', views.CartItemAPI.as_view(), name='cart_item_api'),
    path('checkout_api/', views.CheckoutAPI.as_view(), name='checkout_api'),
    path('cart_api/<int:pk>/', views.CartAPI.as_view(), name='cart_api'),
]
