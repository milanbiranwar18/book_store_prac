from django.db import models

# Create your models here.
from book.models import Book
from user.models import User


class Cart(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('ordered', 'Ordered'),
    )

    total_quantity = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default='active')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def _str_(self):
        return f"{self.user.username}'s Cart"


class CartItem(models.Model):
    quantity = models.IntegerField(default=0)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)

    def _str_(self):
        return f"{self.quantity} x {self.book.title} in {self.cart.user.username}'s Cart"
