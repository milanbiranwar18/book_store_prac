import logging

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.response import Response

from user.models import User

logging.basicConfig(filename="user_serializer.log",
                    filemode='a',
                    format='%(asctime)s %(levelname)s-%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'mobile_num', 'location']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        try:
            return User.objects.create_user(**validated_data)
        except Exception as e:
            logging.error(e)
            return Response({"message": str(e)}, status=400)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

    def create(self, validated_data):
        try:
            user = authenticate(**validated_data)
            if not user:
                raise Exception('Invalid Credentials')
            self.context.update({"user": user})
            return user
        except Exception as e:
            logging.error(e)
            return Response({"message": str(e)}, status=400)
