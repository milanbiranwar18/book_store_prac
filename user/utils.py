from rest_framework.authentication import SessionAuthentication


# class for csrf token error and also did settings in settings.py
class SessionAuth(SessionAuthentication):
    def enforce_csrf(self, request):
        return
    