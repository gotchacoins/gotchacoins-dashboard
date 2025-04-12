from django.utils.translation import get_language

from exchanges.models import UserExchangeKey, Market
from exchanges.clients import EXCHANGE_CLIENTS


def get_portfolio_coins_context(
    user, exchange_id: str, page: int = 1, limit: int = 20
) -> dict:
    try:
        key = UserExchangeKey.objects.get(user=user, exchange__id=exchange_id)
        if exchange_id not in EXCHANGE_CLIENTS:
            return {
                "error_message": f"[{exchange_id}] 지원되지 않는 거래소입니다.",
                "holdings": [],
                "page": page,
                "limit": limit,
                "total": 0,
            }

        client = EXCHANGE_CLIENTS[exchange_id](key.access_key, key.secret_key)
        holdings = client.get_holdings()
        if isinstance(holdings, dict) and holdings.get("error"):
            return {
                "error_message": holdings["message"],
                "holdings": [],
                "page": page,
                "limit": limit,
                "total": 0,
            }

        holdings = client.apply_current_prices(holdings)
        holdings = [item for item in holdings if item["currency"] != "KRW"]

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

            # 💰 수익 계산
            balance = float(item["balance"])
            avg_buy_price = float(item["avg_buy_price"])
            valuation = float(item["valuation"])

            invested_amount = balance * avg_buy_price
            item_profit = valuation - invested_amount
            item_profit_rate = (
                (item_profit / invested_amount * 100) if invested_amount else None
            )

            item["profit"] = item_profit
            item["profit_rate"] = (
                round(item_profit_rate, 2) if item_profit_rate is not None else None
            )

        # 페이지네이션 처리
        total = len(holdings)
        start = (page - 1) * limit
        end = start + limit
        paginated = holdings[start:end]

        return {
            "holdings": paginated,
            "page": page,
            "limit": limit,
            "total": total,
        }

    except UserExchangeKey.DoesNotExist:
        return {
            "error_message": f"{exchange_id.upper()} API 키가 등록되어 있지 않습니다.",
            "holdings": [],
            "page": page,
            "limit": limit,
            "total": 0,
        }


def get_portfolio_summary_context(user, exchange_id: str) -> dict:
    coins_context = get_portfolio_coins_context(user, exchange_id)
    holdings = coins_context.get("holdings", [])

    if "error_message" in coins_context:
        return coins_context

    krw_balance = 0  # 이미 KRW 제거된 상태
    total_valuation = sum(item["valuation"] for item in holdings)
    total_buy_price = sum(
        float(item["balance"]) * float(item["avg_buy_price"]) for item in holdings
    )
    profit = total_valuation - total_buy_price
    profit_rate = (
        round((profit / total_buy_price) * 100, 2) if total_buy_price else None
    )
    total_asset = krw_balance + total_valuation

    return {
        "krw_balance": krw_balance,
        "total_valuation": total_valuation,
        "total_buy_price": total_buy_price,
        "profit": profit,
        "profit_rate": profit_rate,
        "total_asset": total_asset,
    }
