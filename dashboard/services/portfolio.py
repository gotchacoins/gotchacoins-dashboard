from datetime import date

from exchanges.clients import EXCHANGE_CLIENTS

from dashboard.models import PortfolioSnapshot
from dashboard.contexts.portfolio import get_portfolio_summary_context


def save_portfolio_snapshot(user):
    """
    유저의 특정 거래소 포트폴리오 데이터를 스냅샷으로 저장합니다.
    동일한 user + exchange + date 조합이 있을 경우 덮어씌웁니다.
    """
    today = date.today()
    for exchange_id in EXCHANGE_CLIENTS:
        summary = get_portfolio_summary_context(user, exchange_id)

        if "error" in summary:
            continue

        # get_or_create → 이미 저장된 스냅샷 있으면 덮어쓰기 방지
        snapshot, created = PortfolioSnapshot.objects.get_or_create(
            user=user,
            exchange_id=exchange_id,
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
            # 이미 있으면 업데이트
            snapshot.cash_balance = summary["cash_balance"]
            snapshot.total_valuation = summary["total_valuation"]
            snapshot.total_buy_price = summary["total_buy_price"]
            snapshot.profit = summary["profit"]
            snapshot.profit_rate = summary.get("profit_rate")
            snapshot.save()
