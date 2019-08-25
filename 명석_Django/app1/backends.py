from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from app1.models import Member


class EmailBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Member.objects.get(Q(email=username))
        except Member.DoesNotExist:
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user



