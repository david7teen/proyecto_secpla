from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db.models import Q

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None
            
        try:
            # Buscar por email O username
            user = User.objects.get(
                Q(email__iexact=username) | Q(username__iexact=username)
            )
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except User.DoesNotExist:
            return None
        except User.MultipleObjectsReturned:
            # Si hay múltiples, priorizar username exacto
            try:
                user = User.objects.get(username__iexact=username)
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                # Intentar con email exacto
                try:
                    user = User.objects.get(email__iexact=username)
                    if user.check_password(password):
                        return user
                except User.DoesNotExist:
                    return None
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
