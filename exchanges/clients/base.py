from abc import ABC, abstractmethod


class BaseExchangeClient(ABC):
    def __init__(self, access_key: str, secret_key: str):
        self.access_key = access_key
        self.secret_key = secret_key

    @abstractmethod
    def get_holdings(self) -> list[dict]:
        """거래소에서 자산 목록 조회"""
        pass

    @abstractmethod
    def apply_current_prices(self, holdings: list[dict]) -> list[dict]:
        """보유 자산에 현재가 추가"""
        pass
