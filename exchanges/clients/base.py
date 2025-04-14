from abc import ABC, abstractmethod
import httpx


class BaseExchangeClient(ABC):
    def __init__(self, access_key: str = "", secret_key: str = ""):
        self.access_key = access_key
        self.secret_key = secret_key

    def _request(
        self, method: str, path: str, params: dict = None, auth: bool = True
    ) -> dict:
        url = f"{self.BASE_URL}{path}"
        headers = self._generate_headers(params, use_auth=auth)

        try:
            with httpx.Client() as client:
                response = client.request(
                    method, url, headers=headers, params=params, timeout=10
                )
            response.raise_for_status()
            return response.json()

        except httpx.HTTPStatusError as e:
            return self._handle_http_error(e)

        except httpx.RequestError as e:
            return self._error("REQUEST_ERROR", f"요청 실패: {str(e)}")

        except Exception as e:
            return self._error("EXCEPTION", f"알 수 없는 예외: {str(e)}")

    def _error(self, code: str, message: str) -> dict:
        return {
            "error": True,
            "code": code,
            "message": message,
        }

    @abstractmethod
    def _generate_headers(self, query: dict = None, use_auth: bool = True) -> dict:
        """거래소별 인증 방식에 맞는 헤더를 생성"""
        pass

    @abstractmethod
    def _handle_http_error(self, e: httpx.HTTPStatusError) -> dict:
        pass

    @abstractmethod
    def get_holdings(self) -> list[dict]:
        """거래소에서 자산 목록 조회"""
        pass

    @abstractmethod
    def apply_current_prices(self, holdings: list[dict]) -> list[dict]:
        """보유 자산에 현재가 추가"""
        pass
