import jwt
import uuid
import hashlib
from urllib.parse import urlencode

from exchanges.clients.base import BaseExchangeClient
from exchanges.errors.messages import UPBIT_ERROR_CODE_MESSAGES


class UpbitClient(BaseExchangeClient):

    BASE_URL = "https://api.upbit.com"

    def _generate_headers(self, query: dict = None, use_auth: bool = True) -> dict:

        if not use_auth:
            return {}

        payload = {
            "access_key": self.access_key,
            "nonce": str(uuid.uuid4()),
        }

        # 쿼리 파라미터가 있는 경우 query_hash 추가
        if query:
            query_string = urlencode(query)
            query_hash = hashlib.sha512(query_string.encode()).hexdigest()
            payload["query_hash"] = query_hash
            payload["query_hash_alg"] = "SHA512"

        jwt_token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        return {"Authorization": f"Bearer {jwt_token}"}

    def _handle_http_error(self, e) -> dict:
        try:
            error_json = e.response.json()
            upbit_error = (
                error_json.get("error", {}) if isinstance(error_json, dict) else {}
            )
            error_code = upbit_error.get("name", "UNKNOWN")
            message = UPBIT_ERROR_CODE_MESSAGES.get(
                error_code, upbit_error.get("message", "알 수 없는 오류입니다.")
            )

            # 특정 오류코드에 가이드 버튼 표시
            if error_code in UPBIT_ERROR_CODE_MESSAGES.keys():
                return self._error(
                    error_code,
                    message,
                    action_label="가이드 보러가기",
                    action_url="/dashboard/guide/exchange-integration/",
                )

            return self._error(error_code, message)

        except Exception:
            return self._error("UNKNOWN_ERROR", f"응답 파싱 실패: {e.response.text}")

    def get_holdings(self):
        """
        보유 중인 전체 자산 목록을 조회합니다.

        응답 필드:
            - currency (str): 화폐 단위 (KRW, BTC 등)
            - balance (str): 주문 가능 금액/수량
            - locked (str): 주문 중인 금액/수량
            - avg_buy_price (str): 매수 평균가
            - avg_buy_price_modified (bool): 매수 평균가 수정 여부
            - unit_currency (str): 평단가 기준 화폐 (예: KRW)
        """

        return self._request("GET", "/v1/accounts")

    def get_markets(self):
        """
        업비트에서 거래 가능한 종목 목록
        """
        return self._request(
            "GET", "/v1/market/all", params={"is_details": "true"}, auth=False
        )

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

    def enrich_holdings(self, holdings: list[dict]):
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
