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

    def get_price(self, markets: list[str]):
        """
        지정한 마켓의 현재 시세를 조회합니다.

        Args:
            markets (list[str]): 마켓 코드 리스트 (예: ["KRW-BTC", "KRW-ETH"])

        Returns:
            list[dict]: 각 마켓의 현재 시세 정보
        """
        if not markets:
            return []

        joined = ",".join(markets)
        return self._request(
            "GET", "/v1/ticker", params={"markets": joined}, auth=False
        )

    def apply_current_prices(self, holdings: list[dict]):
        markets = [
            f"KRW-{item['currency']}" for item in holdings if item["currency"] != "KRW"
        ]

        prices_data = self.get_price(markets)

        if isinstance(prices_data, dict) and prices_data.get("error"):
            # 에러일 경우 그대로 반환 (원본 holdings 유지)
            return prices_data

        # "BTC": 80000000.0 형식으로 변환
        prices = {
            item["market"].split("-")[1]: item["trade_price"] for item in prices_data
        }

        for item in holdings:
            currency = item["currency"]
            if currency == "KRW":
                item["current_price"] = 1.0
                item["valuation"] = float(item["balance"])
                continue

            price = prices.get(currency, 0)
            item["current_price"] = price
            item["valuation"] = float(item["balance"]) * price

        return holdings
