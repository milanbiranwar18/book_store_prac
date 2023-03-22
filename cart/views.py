import logging

from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart, CartItem
from cart.serializers import CartSerializer, CartItemSerializer2

logging.basicConfig(filename="cart.log",
                    filemode='a',
                    format='%(asctime)s %(levelname)s-%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


# class CartAPI(APIView):
#
#     def post(self, request):
#         """
#         Function for adding books to the cart
#         """
#         try:
#             # print(request.data)
#             request.data.update({"user": request.user.id})
#             # print(request.data)
#             serializer = CartSerializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response({'message': 'Cart Created Successfully', 'data': serializer.data},
#                             status=status.HTTP_201_CREATED)
#         except Exception as e:
#             logging.error(e)
#             return Response({'message': str(e), 'status': 400}, status=status.HTTP_400_BAD_REQUEST)
#
#     def get(self, request):
#         """
#         Function for get carts
#         """
#         try:
#             item_list = Cart.objects.filter(user=request.data.get('user'))
#             print(item_list)
#             serializer = CartSerializer(item_list, many=True)
#             # print(serializer)
#             return Response(serializer.data, status=200)
#         except Exception as e:
#             logging.error(e)
#             return Response({"message": str(e)}, status=400)
#
#     def delete(self, request, pk):
#         """
#         Function for delete cart
#         """
#         try:
#             id = pk
#             cart = Cart.objects.get(pk=id)
#             print(cart)
#             cart.delete()
#             return Response({"Message": "Cart Deleted Successfully", "status": 204})
#         except Exception as e:
#             logging.error(e)
#             return Response({"message": str(e)}, status=400)
#
#
# class CheckoutAPI(APIView):
#
#     def put(self, request):
#         user = Cart.objects.get(user=request.data.get("user"), status=False)
#         print(user)
#         if user is not None:
#             user.status = True
#             user.save()
#             print(user.save())
#         return Response({"Message": "status updated Successfully", 'status': 200})









class AddToCartAPIView(APIView):

    def post(self, request):
        try:
            serializer = CartItemSerializer2(data=request.data, context={"user": request.user})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Book added to cart Successfully", "data":serializer.data, "status":201})
        except Exception as e:
            logging.exception(e)
            return Response({"success": False, "message": e.args[0], "status": 400}, status=400)


class ViewCartAPIView(APIView):
    def get(self, request):
        try:
            user = request.user
            cart = Cart.objects.get(user=user, status='active')
            # cart_item =
            serializer = CartSerializer(cart)
            return Response({"success": True, "message": "Retrieve Cart List Successfully", "data": serializer.data,
                             "status": 200}, status=200)
        except Exception as e:
            logging.exception(e)
            return Response({"success": False, "message": str(e), "status": 400}, status=400)


# class CartItemUpdateView(APIView):
#     def put(self, request, id):
#         cart = Cart.objects.get(user=request.user.id, status='active')
#         cart_item = CartItem.objects.get(id=id, cart_id=cart)
#         cart_item.quantity = request.data.get("quantity")
#         cart_item.save()
#         return JsonResponse({"Message": "Book quantity updated successfully",
#         "data": {"id": cart_item.id, "book": cart_item.book_id, "quantity": cart_item.quantity, "cart_id": cart_item.cart_id}})
#         # return Response({"book":cart_item.book, "qua":cart_item.quantity})


# class CartItemUpdateView(APIView):
#     def put(self, request, id):
#         cart = Cart.objects.get(user=request.user.id, status='active')
#         cart_item = CartItem.objects.get(id=id, cart_id=cart, partial=True)
#         # cart_item.quantity = request.data.get("quantity")
#         # cart_item.save()
#         serializer = CartItemSerializer2(cart_item, request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"message": "Book quantity updated to cart Successfully", "data": serializer.data, "status": 201})
#         # return JsonResponse({"Message": "Book quantity updated successfully", "data": {"id": cart_item.id,
#         #        "book": cart_item.book_id, "quantity": cart_item.quantity, "cart_id": cart_item.cart_id}, "status": 200})
#
#
#     def delete(self, request, id):
#         try:
#             cart = Cart.objects.get(user=request.user.id, status='active')
#             cart_item = CartItem.objects.get(id=id, cart_id=cart)
#             cart_item.delete()
#             return Response({"Message": "Book Item deleted successfully", 'status': 200})
#         except Exception as e:
#             logging.error(e)
#             return Response({"message": str(e)}, status=400)


class CartItemUpdateView(APIView):
    def put(self, request, id):
        try:
            cart = Cart.objects.get(user=request.user.id, status='active')
            cart_item = CartItem.objects.get(id=id, cart_id=cart)
            serializer = CartItemSerializer2(cart_item, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                    {"success": True, "Message": "Book quantity updated successfully",
                     "data": serializer.data, "status": 200}, status=200)
        except Exception as e:
            logging.exception(e)
            return Response({"success": False, "message": e.args[0], "status": 400}, status=400)


class CartItemDeleteView(APIView):
    def delete(self, request, id):
        try:
            cart = Cart.objects.get(user=request.user.id, status='active')
            cart_item = CartItem.objects.get(id=id, cart_id=cart)
            cart = cart.total_quantity - cart_item.quantity
            # cart.save()
            cart = cart.total_price - (cart_item.book_id * cart_item.quantity)
            cart.save()
            cart_item.delete()
            return Response({"Message": "Book Item deleted successfully", 'status': 200})
        except Exception as e:
            logging.error(e)
            return Response({"message": str(e)}, status=400)
