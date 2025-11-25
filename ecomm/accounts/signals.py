from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from .models import Account

@receiver(user_signed_up)
def create_account_social_login(request, user, **kwargs):
    Account.objects.create(
        user=user,
        phone_number="",
        profile_image='../static/images/avatars/avatar1.jpg'
    )