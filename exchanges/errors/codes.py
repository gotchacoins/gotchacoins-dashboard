from enum import Enum


class ExchangeErrorCode(str, Enum):
    EXTERNAL_API_ERROR = "EXTERNAL_API_ERROR"  # 거래소 서버 오류
    KEY_MISSING = "KEY_MISSING"  # API 키 등록이 안되었을 경우
    NOT_SUPPORTED_EXCHANGE = "NOT_SUPPORTED_EXCHANGE"  # 지원하는 거래소가 아닐 경우
    UNKNOWN_ERROR = "UNKNOWN_ERROR"  # 알 수 없는 에러
