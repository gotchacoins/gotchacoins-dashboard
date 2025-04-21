from datetime import date

from exchanges.clients import EXCHANGE_CLIENTS

from dashboard.models import PortfolioSnapshot
from dashboard.contexts.portfolio import get_portfolio_summary_context


def save_portfolio_snapshot(user, exchange_id: str = None):
    """
    유저의 포트폴리오 데이터를 스냅샷으로 저장합니다.
    - exchange_id가 주어지면 해당 거래소만 저장
    - 없으면 등록된 전체 거래소에 대해 저장
    """
    today = date.today()
    exchange_ids = [exchange_id] if exchange_id else EXCHANGE_CLIENTS.keys()

    for ex_id in exchange_ids:
        summary = get_portfolio_summary_context(user, ex_id)

        if "error" in summary:
            continue

        snapshot, created = PortfolioSnapshot.objects.get_or_create(
            user=user,
            exchange_id=ex_id,
            date=today,
            defaults={
                "cash_balance": summary["cash_balance"],
                "total_valuation": summary["total_valuation"],
                "total_buy_price": summary["total_buy_price"],
                "profit": summary["profit"],
                "profit_rate": summary.get("profit_rate"),
            },
        )

        if not created:
            snapshot.cash_balance = summary["cash_balance"]
            snapshot.total_valuation = summary["total_valuation"]
            snapshot.total_buy_price = summary["total_buy_price"]
            snapshot.profit = summary["profit"]
            snapshot.profit_rate = summary.get("profit_rate")
            snapshot.save()
