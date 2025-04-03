from allauth.account.signals import user_signed_up
from django.dispatch import receiver


@receiver(user_signed_up)
def save_avatar_from_social_login(request, user, **kwargs):
    sociallogin = kwargs.get("sociallogin")
    if not sociallogin:
        return

    provider = sociallogin.account.provider
    data = sociallogin.account.extra_data

    avatar_url = get_avatar_url_from_provider(provider, data)

    if avatar_url:
        user.avatar_url = avatar_url
        user.save()


def get_avatar_url_from_provider(provider: str, data: dict) -> str | None:
    if provider == "google":
        return data.get("picture")
    # elif provider == "github":
    #     return data.get("avatar_url")
    # elif provider == "facebook":
    #     return data.get("picture", {}).get("data", {}).get("url")
    # return None

    # 만약 엄청 많아질 경우 아래와 같이도 매핑하는 방식도 가능
    # AVATAR_FIELD_MAP = {
    #     "google": lambda d: d.get("picture"),
    #     "github": lambda d: d.get("avatar_url"),
    #     "facebook": lambda d: d.get("picture", {}).get("data", {}).get("url"),
    # }
    # def get_avatar_url_from_provider(provider: str, data: dict) -> str | None:
    #     parser = AVATAR_FIELD_MAP.get(provider)
    #     return parser(data) if parser else None
