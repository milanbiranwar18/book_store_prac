# Create your views here.
import logging

from django.contrib.auth import logout, login
from rest_framework.response import Response
from rest_framework.views import APIView

from user.serializer import LoginSerializer, RegistrationSerializer

logging.basicConfig(filename="user.log",
                    filemode='a',
                    format='%(asctime)s %(levelname)s-%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class UserRegistration(APIView):

    def post(self, request):
        try:
            serializer = RegistrationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"Message": "User registered successfully", "data": serializer.data, 'status': 201})
        except Exception as e:
            logging.error(e)
            return Response({"message": str(e)}, status=400)


class UserLogin(APIView):

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            login(request, serializer.context.get("user"))
            return Response({"Message": "User login successfully", 'status': 201})
        except Exception as e:
            logging.error(e)
            return Response({"message": str(e)}, status=400)


class UserLogout(APIView):

    def get(self, request):
        try:
            if request.user.is_authenticated:
                logout(request)
                return Response({"Message": "User logout successfully"}, status=201)
        except Exception as e:
            logging.error(e)
            return Response({"message": str(e)}, status=400)
