from django.contrib.auth.backends import BaseBackend
from .models import AdminAccounts

class AdminAccountsBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = AdminAccounts.objects.get(username=username)
            if user.check_password(password):
                return user
        except AdminAccounts.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return AdminAccounts.objects.get(pk=user_id)
        except AdminAccounts.DoesNotExist:
            return None