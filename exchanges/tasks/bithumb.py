from celery import shared_task
from exchanges.models import Exchange, Market
from exchanges.clients.bithumb import BithumbClient


@shared_task
def sync_bithumb_markets_task():
    client = BithumbClient()  # public endpoint이므로 키 없이 가능
    data = client.get_markets()

    if isinstance(data, dict) and data.get("error"):
        print(f"[Bithumb] 마켓 동기화 실패: {data['message']}")
        return

    exchange, _ = Exchange.objects.get_or_create(
        id="bithumb", defaults={"name": "빗썸", "base_url": client.BASE_URL}
    )

    created, updated = 0, 0
    for item in data:

        market_code = item["market"]  # 예: KRW-BTC
        base_currency, quote_currency = (
            market_code.split("-")[1],
            market_code.split("-")[0],
        )

        warning_flag = item.get("market_warning")
        market_warning = "경고" if warning_flag and warning_flag != "NONE" else ""

        obj, is_created = Market.objects.update_or_create(
            exchange=exchange,
            market=market_code,
            defaults={
                "base_currency": base_currency,
                "quote_currency": quote_currency,
                "korean_name": item["korean_name"],
                "english_name": item["english_name"],
                "market_warning": market_warning,
            },
        )
        if is_created:
            created += 1
        else:
            updated += 1

    print(f"[Bithumb] 마켓 동기화 완료: 생성 {created}개, 수정 {updated}개")
