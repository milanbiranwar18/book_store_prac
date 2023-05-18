import logging

import jwt as jwt
from rest_framework.authentication import SessionAuthentication


# class for csrf token error and also did settings in settings.py
from rest_framework.response import Response

from book_store import settings


class SessionAuth(SessionAuthentication):
    def enforce_csrf(self, request):
        return


logging.basicConfig(filename="utils.log",
                    filemode='a',
                    format='%(asctime)s %(levelname)s-%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class JWT:
    """
    Class for JWT
    """
    def encode(self, data):
        try:
            if not isinstance(data, dict):
                return Response({"Message":"Data should be a dictionary"})
            if 'exp' not in data.keys():
                data.update({'exp': settings.JWT_EXP})
            return jwt.encode(data, 'secret', algorithm='HS256')
        except Exception as e:
            logging.error(e)

    def decode(self, token):
        try:
            return jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.exceptions.ExpiredSignatureError:
            return Response({"Message":"Token Expired"})
        except jwt.exceptions.InvalidTokenError:
            return Response({"Message":"Invalid Token"})
        except Exception as e:
            logging.error(e)


def verify_token(function):
    def wrapper(self, request, *args, **kwargs):

        token = request.headers.get("Token")
        if not token:
            return Response({"Message":"Token not found"}, status=400)
        decoded = JWT().decode(token)
        if not decoded:
            return Response({"Message":"Token Authentication required"})
        user_id = decoded.get("user_id")
        if not user_id:
            return Response({"Message":"Invalid user"}, status=400)
        # request.POST._mutable = True
        request.data.update({"user": user_id})
        # request.POST._mutable = False

        # # remember old state
        # _mutable = request.data._mutable
        #
        # # set to mutable
        # request.data._mutable = True
        #
        # # сhange the values you want
        # request.data.update({"user": user_id})
        #
        # # set mutable flag back
        # request.data._mutable = _mutable

        return function(self, request, *args, **kwargs)
    return wrapper

