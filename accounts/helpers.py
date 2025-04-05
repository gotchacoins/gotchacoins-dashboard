def get_name_and_avatar(provider, data):
    first_name = None
    last_name = None
    avatar_url = None

    if provider == "google":
        first_name = data.get("given_name")
        last_name = data.get("family_name")
        avatar_url = data.get("picture")

    # elif provider == "kakao":
    #     props = data.get("properties", {})
    #     first_name = props.get("nickname")
    #     avatar_url = props.get("profile_image")

    elif provider == "naver":
        first_name = data.get("name")
        avatar_url = data.get("profile_image")

    return first_name, last_name, avatar_url
