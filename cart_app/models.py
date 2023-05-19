from django.db import models

# Create your models here.
from book.models import Book
from user.models import User


class UserCart(models.Model):
    total_quantity = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    status = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class UserCartItem(models.Model):
    quantity = models.IntegerField()
    cart = models.ForeignKey(UserCart, on_delete=models.CASCADE, related_name='cart_items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)


