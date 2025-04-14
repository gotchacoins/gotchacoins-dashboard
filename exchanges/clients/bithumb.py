import jwt
import uuid
import time

from exchanges.clients.base import BaseExchangeClient
from exchanges.errors.messages import BITHUMB_ERROR_CODE_MESSAGES


class BithumbClient(BaseExchangeClient):

    BASE_URL = "https://api.bithumb.com"

    def _generate_headers(self, query: dict = None, use_auth: bool = True) -> dict:

        if not use_auth:
            return {}

        payload = {
            "access_key": self.access_key,
            "nonce": str(uuid.uuid4()),
            "timestamp": round(time.time() * 1000),
        }

        jwt_token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        return {"Authorization": f"Bearer {jwt_token}"}

    def _handle_http_error(self, e):
        try:
            error_json = e.response.json()
            bithumb_error = (
                error_json.get("error", {}) if isinstance(error_json, dict) else {}
            )
            error_code = bithumb_error.get("name", "UNKNOWN")
            message = BITHUMB_ERROR_CODE_MESSAGES.get(
                error_code, bithumb_error.get("message", "알 수 없는 오류입니다.")
            )
            return self._error(error_code, message)

        except Exception:
            return self._error("UNKNOWN_ERROR", f"응답 파싱 실패: {e.response.text}")

    def get_holdings(self):
        return self._request("GET", "/v1/accounts")
