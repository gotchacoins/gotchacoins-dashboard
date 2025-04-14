from .upbit import UpbitClient
from .bithumb import BithumbClient

EXCHANGE_CLIENTS = {
    "upbit": UpbitClient,
    "bithumb": BithumbClient,
}
