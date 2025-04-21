from django.utils.translation import get_language
from django.utils.timezone import now, localtime

from exchanges.clients.base import BaseExchangeClient
from exchanges.errors.codes import ExchangeErrorCode
from exchanges.models import UserExchangeKey, Market

from exchanges.clients import EXCHANGE_CLIENTS
from exchanges.constants import CASH_CURRENCIES


def get_portfolio_coins_context(
    user, exchange_id: str, page: int = 1, limit: int = 20
) -> dict:
    try:
        if exchange_id not in EXCHANGE_CLIENTS:
            return {
                "error": {
                    "code": ExchangeErrorCode.NOT_SUPPORTED_EXCHANGE,
                    "message": f"🚫 [{exchange_id}] 지원되지 않는 거래소입니다.",
                },
                "exchange_id": exchange_id,
                "holdings": [],
                "page": page,
                "limit": limit,
                "total": 0,
            }

        key = UserExchangeKey.objects.get(user=user, exchange__id=exchange_id)

        client: BaseExchangeClient = EXCHANGE_CLIENTS[exchange_id](
            key.access_key, key.secret_key
        )
        holdings = client.get_holdings()
        if isinstance(holdings, dict) and holdings.get("error"):
            error = {
                "code": holdings.get("code", ExchangeErrorCode.EXTERNAL_API_ERROR),
                "message": holdings.get("message", "외부 API 호출 오류입니다."),
            }

            # 버튼이 포함되어 있다면 같이 전달
            if holdings.get("action_label") and holdings.get("action_url"):
                error["action_label"] = holdings["action_label"]
                error["action_url"] = holdings["action_url"]

            return {
                "error": error,
                "exchange_id": exchange_id,
                "holdings": [],
                "page": page,
                "limit": limit,
                "total": 0,
            }

        holdings = client.enrich_holdings(holdings)
        cash_item = next(
            (item for item in holdings if item["currency"] in CASH_CURRENCIES), None
        )
        cash_balance = float(cash_item["balance"]) if cash_item else 0.0

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

        # 원화, 달러 코인 목록에서 제거
        filtered_holdings = [
            item for item in holdings if item["currency"] not in CASH_CURRENCIES
        ]

        key.last_updated = now()
        key.save(update_fields=["last_updated"])

        # 페이지네이션 처리
        total = len(filtered_holdings)
        start = (page - 1) * limit
        end = start + limit
        paginated = filtered_holdings[start:end]

        return {
            "exchange_id": exchange_id,
            "holdings": paginated,
            "page": page,
            "limit": limit,
            "total": total,
            "cash_balance": cash_balance,
            "last_updated": localtime(key.last_updated).strftime("%Y-%m-%d %H:%M:%S"),
        }

    except UserExchangeKey.DoesNotExist:
        return {
            "error": {
                "code": ExchangeErrorCode.KEY_MISSING,
                "message": f"🚫 {exchange_id.upper()} API 키가 등록되어 있지 않습니다.",
                "action_label": "거래소 연동하기",
                "action_url": "/dashboard/exchange-settings/",
            },
            "holdings": [],
            "exchange_id": exchange_id,
            "page": page,
            "limit": limit,
            "total": 0,
        }


def get_portfolio_summary_context(user, exchange_id: str) -> dict:
    coins_context = get_portfolio_coins_context(user, exchange_id)
    holdings = coins_context.get("holdings", [])

    if "error" in coins_context:
        return {
            "cash_balance": 0,
            "total_valuation": 0,
            "total_buy_price": 0,
            "profit": 0,
            "profit_rate": 0,
            "total_asset": 0,
            "error": coins_context["error"],
        }

    cash_balance = coins_context.get("cash_balance", 0.0)
    total_valuation = sum(item["valuation"] for item in holdings)
    total_buy_price = sum(
        float(item["balance"]) * float(item["avg_buy_price"]) for item in holdings
    )
    profit = total_valuation - total_buy_price
    profit_rate = (
        round((profit / total_buy_price) * 100, 2) if total_buy_price else None
    )
    total_asset = cash_balance + total_valuation

    return {
        "exchange_id": exchange_id,
        "cash_balance": cash_balance,  # 보유 현금
        "total_valuation": total_valuation,  # 총 평가금액
        "total_buy_price": total_buy_price,  # 총 매수금액
        "profit": profit,  # 총 수익
        "profit_rate": profit_rate,  # 총 수익률
        "total_asset": total_asset,  # 총 자산 (보유현금 + 총 평가금액)
        "last_updated": coins_context.get("last_updated"),
    }
