from allauth.account.signals import user_signed_up
from django.dispatch import receiver

from .helpers import get_name_and_avatar


@receiver(user_signed_up)
def populate_user_from_sociallogin(request, user, **kwargs):
    sociallogin = kwargs.get("sociallogin")
    if not sociallogin:
        return

    provider = sociallogin.account.provider
    data = sociallogin.account.extra_data

    first_name, last_name, avatar = get_name_and_avatar(provider, data)

    if first_name and not user.first_name:
        user.first_name = first_name
    if last_name and hasattr(user, "last_name") and not user.last_name:
        user.last_name = last_name
    if avatar and hasattr(user, "avatar") and not user.avatar:
        user.avatar = avatar

    user.save()
