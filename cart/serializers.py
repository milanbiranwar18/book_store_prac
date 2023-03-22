from rest_framework import serializers

from book.models import Book
from cart.models import Cart, CartItem


# class CartItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CartItem
#         fields = ['id', 'quantity', 'book', 'cart']
#         # required_field = ['quantity', 'cart']
#
#
# class DataSerializer(serializers.Serializer):
#
#     book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
#     quantity = serializers.IntegerField()
#
#
# class CartSerializer(serializers.ModelSerializer):
#
#     books = DataSerializer(many=True, write_only=True)
#     cartitem = CartItemSerializer(many=True, read_only=True)
#
#
#     class Meta:
#         model = Cart
#         fields = ['id', 'total_price', 'status', 'user', 'total_quantity', 'books', 'cartitem']
#         read_only_fields = ['total_price', 'status', 'total_quantity']
#
#     print("hello milan")
#     def create(self, validated_data):
#         print(validated_data)
#         user = validated_data.get('user')
#         print(user.id)
#         book_list = validated_data.get("books")
#         print(123456)
#         cart = Cart.objects.filter(user_id=user.id)
#         print(len(cart))
#         if len(cart) != 0:
#             print(122)
#             total_quantity = 0
#             total_price = 0
#             for book_dict in book_list:
#                 total_quantity = 0
#                 book_id = book_dict.get('book_id')
#                 quantity = book_dict.get('quantity')
#                 book = Book.objects.get("book_id")
#                 cart_item = CartItem.objects.create(book_id=book_id, quantity=quantity, cart_id=cart.id)
#                 total_quantity += cart_item.quantity
#                 book_price = quantity * book.price
#                 total_price += book_price
#             cart = Cart.objects.update(user_id=user.id, total_quantity=total_quantity, total_price=total_price,
#                                        default='active')
#
#
#         else:
#             print(12345, "hello")
#             total_quantity = 0
#             total_price = 0
#             cart = Cart.objects.create(user_id=user.id, total_quantity=total_quantity, total_price=total_price,
#                                        default='active')
#             print(cart.id)
#             for book_dict in book_list:
#                 print(book_dict, 123456879)
#                 total_quantity = 0
#                 book_id = book_dict.get('book_id')
#                 quantity = book_dict.get('quantity')
#                 book = Book.objects.get("book_id")
#                 print(book, "bookid")
#                 cart_item = CartItem.objects.create(book_id=book_id, quantity=quantity, cart_id=cart.id)
#                 print(cart_item, 'cartitem')
#                 total_quantity += cart_item.quantity
#                 book_price = quantity * book.price
#                 total_price += book_price
#             cart = Cart.objects.update(user_id=user.id, total_quantity=total_quantity, total_price=total_price,
#                                        default='active')
#         return cart


# class DataSerializer(serializers.Serializer):
#     book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
#     quantity = serializers.IntegerField(default=1)

class CartItemSerializer2(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
    quantity = serializers.IntegerField(default=0)

    class Meta:
        model = CartItem
        fields = ['id', 'book', 'quantity', 'cart']
        read_only_fields = ['cart']

    def create(self, validated_data):
        user = self.context.get('user')
        book = validated_data.get('book')
        quantity = validated_data.get('quantity')

        try:
            cart = Cart.objects.get(user=user, status='active')
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=user, status='active')

        cart_item = CartItem.objects.filter(cart=cart, book=book).first()
        if cart_item is not None:
            cart_item.quantity += quantity
            cart.save()
        else:
            cart_item = CartItem.objects.create(cart=cart, book=book, quantity=quantity)
        cart.total_quantity += quantity
        cart.total_price += book.price * quantity
        cart.save()
        return cart_item

    def update(self, instance, validated_data):
        # Get the new quantity from the validated data
        quantity = validated_data.get('quantity')
        if quantity == 0:
            instance.delete()

        # Set the new quantity on the instance and save it
        instance.quantity = quantity
        instance.save()

        # Update cart total_quantity and total_price
        cart_items = CartItem.objects.filter(cart=instance.cart)
        instance.cart.total_quantity = sum([item.quantity for item in cart_items])
        instance.cart.total_price = sum([item.book.price * item.quantity for item in cart_items])
        instance.cart.save()

        # Return the updated instance

        return instance

# class CartSerializer(serializers.ModelSerializer):
#     # items = CartItemSerializer2(many=True, read_only=True)
#     items = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Cart
#         fields = ('total_quantity', 'total_price', 'status', 'items')
#
#     def get_items(self, obj):
#         # Get all cart items in the cart
#         cart_items = CartItem.objects.filter(cart=obj)
#
#         # Create a dictionary to store each unique book item and its quantity
#         unique_items = {}


class CartSerializer(serializers.ModelSerializer):
    # items = CartItemSerializer2(many=True, read_only=True)
    items = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'total_quantity', 'total_price', 'status', 'items']

    def get_items(self, obj):
        # Get all cart items in the cart
        cart_items = CartItem.objects.filter(cart=obj)

        # Create a dictionary to store each unique book item and its quantity
        unique_items = {}

        # Iterate over the cart items and update the quantity of the unique items(only for quantity get cart list)
        for item in cart_items:
            key = (item.book.id, item.book.title, item.book.author, item.book.price)
            if key in unique_items:
                unique_items[key]['quantity'] += item.quantity
            else:
                unique_items[key] = {'item_id':item.id,
                                     'book_id': item.book.id,
                                     'title': item.book.title,
                                     'author': item.book.author,
                                     'price': item.book.price,
                                     'quantity': item.quantity}

            # Return the list of unique book items
            return list(unique_items.values())

    # def update(self, instance, validated_data):
    #     # Get the request data
    #     request = self.context.get('request')
    #     quantity = validated_data.get('quantity')
    #
    #     # Get the cart item
    #     cart_item = CartItem.objects.get(pk=self.instance['id'])
    #
    #     # Calculate the price difference between the old and new quantity
    #     price_diff = (quantity - cart_item.quantity) * cart_item.book.price
    #
    #     # Update the cart item and cart
    #     cart_item.quantity = quantity
    #     cart_item.save()
    #     instance.total_quantity += quantity - cart_item.quantity
    #     instance.total_price += price_diff
    #     instance.save()
    #
    #     return instance




# class CartItemSerializer2(serializers.ModelSerializer):
#     quantity = serializers.IntegerField(default=1)
#
#
#     class Meta:
#         model = CartItem
#         fields = ('book', 'quantity')
#
#     # def validate(self, attrs):
#     #     try:
#     #         print(attrs)
#     #         book_id = attrs['book']
#     #         attrs['book'] = Book.objects.get(pk=book_id)
#     #     except Book.DoesNotExist:
#     #         raise serializers.ValidationError(detail="Book does not exist")
#     #     return attrs
#
#     @staticmethod
#     def add_to_cart(cart: Cart, validated_data:dict):
#
#         print('============================')
#         print(validated_data)
#         print('============================')
#         quantity = validated_data.get('quantity')
#         book: Book = validated_data.get('book')
#         try:
#             cart_item = CartItem.objects.get(cart=cart, book=book)
#             cart_item.quantity += quantity
#             cart_item.save()
#         except CartItem.DoesNotExist:
#             cart_item = CartItem.objects.create(cart=cart, book=book, quantity=quantity)
#
#         cart.total_quantity += quantity
#         cart.total_price += book.price * quantity
#         cart.save()
#         return cart_item
#
#     def create(self, validated_data):
#         user = self.context.get('user')
#         try:
#             # Try to retrieve an existing cart for the user
#             cart = Cart.objects.get(user=user, status='active') # noqa
#         except Cart.DoesNotExist: # noqa
#             # If a cart does not exist, create a new one
#             cart = Cart.objects.create(user=user, status='active') # noqa
#         cart_item = self.add_to_cart(cart, validated_data)
#         return cart_item
