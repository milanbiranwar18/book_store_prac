from rest_framework import serializers
from book.models import Book
from cart_app.models import UserCart, UserCartItem


class CartItemSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = UserCartItem
        fields = ['id', 'quantity', 'book', 'cart']
        read_only_fields = ['cart']

    def create(self, validated_data):
        user = self.context.get('user')

        book = validated_data.get('book')

        quantity = validated_data.get('quantity')

        cart_list = UserCart.objects.filter(user_id=user.id, status=False)

        if len(cart_list) == 0:
            cart = UserCart.objects.create(user_id=user.id)
        else:
            cart = cart_list.first()
        cart_item_list = UserCartItem.objects.filter(book_id=book.id,  cart_id=cart.id)

        if len(cart_item_list) == 0:
            cart_item = UserCartItem.objects.create(book_id=book.id, quantity=quantity, cart_id=cart.id)
            book_price = book.price * quantity
            cart.total_price += book_price
            cart.total_quantity += quantity
            cart.save()
        else:
            cart_item = cart_item_list.first()
            cart_item.quantity += quantity
            cart_item.save()
            books_price = quantity * book.price
            cart.total_price += books_price
            cart.total_quantity += quantity
            cart.save()

        return cart_item


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserCart
        fields = ['id', 'total_price', "total_quantity", 'status', 'user']
