import secrets
import string

# Django의 기본 SECRET_KEY에 사용되는 문자 집합: 소문자, 숫자, 그리고 일부 특수문자
ALLOWED_CHARS: str = string.ascii_lowercase + string.digits + "!@#$%^&*(-_=+)"

def generate_django_secret_key(length: int = 50) -> str:
    """
    안전한 DJANGO_SECRET_KEY를 생성하는 함수입니다.
    """
    return ''.join(secrets.choice(ALLOWED_CHARS) for _ in range(length))

def run() -> None:
    secret_key: str = generate_django_secret_key()
    print(f"생성된 Django SECRET_KEY:\n{secret_key}")
