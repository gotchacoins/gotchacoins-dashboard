# exchanges/clients/upbit.py

import uuid
import jwt
import httpx

UPBIT_API_URL = "https://api.upbit.com"


def get_upbit_balances(access_key: str, secret_key: str) -> list:
    """
    업비트 API 키로 사용자 잔고 조회
    Returns:
        list: [{ currency, balance, avg_buy_price, ... }]
    """
    try:
        payload = {
            "access_key": access_key,
            "nonce": str(uuid.uuid4()),
        }

        jwt_token = jwt.encode(payload, secret_key, algorithm="HS256")
        headers = {
            "Authorization": f"Bearer {jwt_token}",
        }

        with httpx.Client() as client:
            response = client.get(
                f"{UPBIT_API_URL}/v1/accounts", headers=headers, timeout=10
            )

        if response.status_code == 200:
            return response.json()
        else:
            print(f"[Upbit] 오류 응답: {response.status_code}, {response.text}")
            return []

    except Exception as e:
        print(f"[Upbit] 예외 발생: {e}")
        return []
