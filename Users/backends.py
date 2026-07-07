# Users/backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailOrUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            return None
            
        # If the typed input contains an @ symbol, search via the email column
        if '@' in username:
            kwargs = {'email__iexact': username}  # iexact makes it case-insensitive
        else:
            kwargs = {'username__iexact': username}
            
        try:
            user = User.objects.get(**kwargs)
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except User.DoesNotExist:
            return None
