import uuid
from django.contrib.auth import get_user_model

User = get_user_model()


def generate_unique_username(email=None):
    """
    이메일이 주어지면 이메일의 local part를 기반으로 유저 이름 생성.
    없으면 uuid 기반 랜덤 유저 이름 생성.
    항상 username 중복을 방지함.
    """
    base = "user"
    if email:
        base = email.split("@")[0]
        base = base[:15].lower().replace(".", "").replace("_", "")

    while True:
        suffix = uuid.uuid4().hex[:4]  # 중복 방지용 4자리
        username = f"{base}_{suffix}"

        if not User.objects.filter(username=username).exists():
            return username
