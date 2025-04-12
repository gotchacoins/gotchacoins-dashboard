from exchanges.models import UserExchangeKey, Market
from django.utils.translation import get_language
from exchanges.clients import EXCHANGE_CLIENTS


def get_portfolio_context(user, exchange_id: str) -> dict:
    context = {}

    try:
        key = UserExchangeKey.objects.get(user=user, exchange__id=exchange_id)

        # 지원 여부 확인
        if exchange_id not in EXCHANGE_CLIENTS:
            return {
                "error_message": f"[{exchange_id}] 아직 지원되지 않는 거래소입니다.",
                "holdings": [],
            }

        # 거래소 클라이언트 생성
        ClientClass = EXCHANGE_CLIENTS[exchange_id]
        client = ClientClass(key.access_key, key.secret_key)

        holdings = client.get_holdings()
        if isinstance(holdings, dict) and holdings.get("error"):
            return {"error_message": holdings["message"], "holdings": []}

        holdings = client.apply_current_prices(holdings)
        holdings = [item for item in holdings if item["currency"] != "KRW"]

        # 이름 매핑 (선택 사항)
        language_code = get_language()
        markets = Market.objects.filter(exchange__id=exchange_id)
        market_dict = {m.base_currency: m for m in markets}
        for item in holdings:
            market = market_dict.get(item["currency"])
            item["name"] = (
                (market.english_name if language_code == "en" else market.korean_name)
                if market
                else item["currency"]
            )

        # KPI 계산
        krw_balance = next(
            (float(item["balance"]) for item in holdings if item["currency"] == "KRW"),
            0,
        )
        total_valuation = sum(
            item["valuation"] for item in holdings if item["currency"] != "KRW"
        )
        total_buy_price = sum(
            float(item["balance"]) * float(item["avg_buy_price"])
            for item in holdings
            if item["currency"] != "KRW"
        )
        profit = total_valuation - total_buy_price
        profit_rate = (
            round((profit / total_buy_price) * 100, 2) if total_buy_price else None
        )
        total_asset = krw_balance + total_valuation

        context.update(
            {
                "holdings": holdings,
                "total_valuation": total_valuation,
                "total_buy_price": total_buy_price,
                "profit": profit,
                "profit_rate": profit_rate,
                "krw_balance": krw_balance,
                "total_asset": total_asset,
            }
        )

    except UserExchangeKey.DoesNotExist:
        context.update(
            {
                "error_message": f"{exchange_id.upper()} API 키가 등록되어 있지 않습니다.",
                "holdings": [],
            }
        )

    return context
