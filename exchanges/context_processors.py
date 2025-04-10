from exchanges.models import UserExchangeKey


def is_exchange_connected(request):
    """
    현재 사용자가 하나 이상의 거래소와 연동되어 있는지 확인합니다.
    """
    if not request.user.is_authenticated:
        return {"is_exchange_connected": False}

    return {
        "is_exchange_connected": UserExchangeKey.objects.filter(
            user=request.user, is_active=True
        )
        .only("id")
        .exists()
    }
