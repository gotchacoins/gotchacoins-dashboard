from exchanges.clients import EXCHANGE_CLIENTS
from dashboard.contexts.portfolio import get_portfolio_summary_context


def get_dashboard_summary_context(user) -> dict:
    cash_total = 0.0
    total_valuation = 0.0
    total_buy_price = 0.0
    updated_times = []

    for exchange_id in EXCHANGE_CLIENTS:
        summary = get_portfolio_summary_context(user, exchange_id)

        if "error" in summary:
            return {
                "cash_balance": 0,
                "total_valuation": 0,
                "total_buy_price": 0,
                "profit": 0,
                "profit_rate": 0,
                "total_asset": 0,
            }

        # 누적 데이터 집계
        cash_total += summary.get("cash_balance", 0.0)
        total_valuation += summary.get("total_valuation", 0.0)
        total_buy_price += summary.get("total_buy_price", 0.0)

        # 각 거래소의 last_updated 모으기
        if summary.get("last_updated"):
            updated_times.append(summary["last_updated"])

    profit = total_valuation - total_buy_price
    profit_rate = (
        round((profit / total_buy_price) * 100, 2) if total_buy_price else None
    )
    total_asset = cash_total + total_valuation

    # 가장 최신의 갱신 시각 하나만 표시
    last_updated = max(updated_times) if updated_times else None

    return {
        "cash_balance": round(cash_total, 2),
        "total_valuation": round(total_valuation, 2),
        "total_buy_price": round(total_buy_price, 2),
        "profit": round(profit, 2),
        "profit_rate": profit_rate,
        "total_asset": round(total_asset, 2),
        "last_updated": last_updated,
    }
