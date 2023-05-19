import logging

from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from cart_app.models import UserCart, UserCartItem
from cart_app.serializers import CartItemSerializer, CartSerializer

logging.basicConfig(filename="cart_view.log",
                    filemode='a',
                    format='%(asctime)s %(levelname)s-%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class CartItemAPI(APIView):

    def post(self, request):
        try:
            request.data.update({"user": request.user.id})
            serializer = CartItemSerializer(data=request.data, context={"user": request.user})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'Cart Item Added Successfully', 'data': serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(e)
            return Response({'message': str(e), 'status': 400}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id):
        try:
            cart = UserCart.objects.get(id = id)
            cart_serializer = CartSerializer(cart, many=False)
            return Response({"Message": "List of Cart Items", "cart data": cart_serializer.data, "status": 200})
        except Exception as e:
            logging.error(e)
            return Response({"message": str(e)}, status=400)

    def delete(self, request, id):
        try:
            cart_item = UserCartItem.objects.get(id=id)
            cart_item.delete()
            return Response({"Message": "Cart Item Deleted Successfully", "status": 204})
        except Exception as e:
            logging.error(e)
            return Response({"message": str(e)}, status=400)


class CheckoutAPI(APIView):

    def put(self, request):
        user = UserCart.objects.get(user_id=request.user.id, status=False)
        if user is not None:
            user.status = True
            user.save()
        return Response({"Message": "status updated Successfully", 'status': 200})


class CartAPI(APIView):

    def delete(self, request, pk):
        try:
            cart = UserCart.objects.get(id=pk)
            cart.delete()
            return Response({"Message": "Cart Deleted Successfully", "status": 204})
        except Exception as e:
            logging.error(e)
            return Response({"message": str(e)}, status=400)
