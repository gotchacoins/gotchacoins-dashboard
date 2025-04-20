from exchanges.clients import EXCHANGE_CLIENTS
from dashboard.contexts.portfolio import get_portfolio_summary_context


def get_dashboard_summary_context(user) -> dict:
    cash_total = 0.0
    total_valuation = 0.0
    total_buy_price = 0.0

    for exchange_id in EXCHANGE_CLIENTS:
        summary = get_portfolio_summary_context(user, exchange_id)

        if "error" in summary:
            continue

        # 개별 거래소 기준 데이터 누적
        cash_total += summary.get("cash_balance", 0.0)
        total_valuation += summary.get("total_valuation", 0.0)
        total_buy_price += summary.get("total_buy_price", 0.0)

    profit = total_valuation - total_buy_price
    profit_rate = (
        round((profit / total_buy_price) * 100, 2) if total_buy_price else None
    )
    total_asset = cash_total + total_valuation

    return {
        "cash_balance": round(cash_total, 2),
        "total_valuation": round(total_valuation, 2),
        "total_buy_price": round(total_buy_price, 2),
        "profit": round(profit, 2),
        "profit_rate": profit_rate,
        "total_asset": round(total_asset, 2),
    }
