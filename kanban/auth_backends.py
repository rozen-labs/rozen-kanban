from __future__ import annotations

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()

class LocalAuthenticationBackend(ModelBackend):
    """Authenticate local users by username or email.

    LDAP/AD can be added later by registering another Django auth backend
    without changing views, forms, or permission checks.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        identifier = username or kwargs.get("email")
        if not identifier or password is None:
            return None
        query = {"username__iexact": identifier} if "@" not in identifier else {"email__iexact": identifier}
        try:
            user = User.objects.get(**query)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email__iexact=identifier)
            except User.DoesNotExist:
                return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
