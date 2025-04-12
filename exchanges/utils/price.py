from exchanges.models import Market


def get_upbit_market_codes(currencies: list[str]) -> dict[str, str]:
    """
    주어진 base_currency 리스트에 대해 KRW 마켓 코드를 반환합니다.

    Returns:
        dict[str, str]: {"BTC": "KRW-BTC", ...}
    """
    qs = Market.objects.filter(
        exchange__id="upbit",
        base_currency__in=currencies,
        quote_currency="KRW",
    ).values_list("base_currency", "market")

    return dict(qs)
