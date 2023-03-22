from django.urls import path

from . import views

urlpatterns = [
    # path('cart_api/', views.CartAPI.as_view(), name='cart_api'),
    # path('cart_api/<int:pk>/', views.CartAPI.as_view(), name='cart_api'),
    # path('checkout_api/', views.CheckoutAPI.as_view(), name='checkout_api'),

    path('view-cart/', views.ViewCartAPIView.as_view(), name='view-cart'),
    path('add_item-cart/', views.AddToCartAPIView.as_view(), name='add_item-cart'),
    path('update_item-cart/<int:id>/', views.CartItemUpdateView.as_view(), name='update_item-cart'),
    path('delete_item-cart/<int:id>/', views.CartItemDeleteView.as_view(), name='update_item-cart'),



]