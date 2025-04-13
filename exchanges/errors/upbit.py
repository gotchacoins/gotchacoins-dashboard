# https://docs.upbit.com/kr/docs/api-%EC%A3%BC%EC%9A%94-%EC%97%90%EB%9F%AC-%EC%BD%94%EB%93%9C-%EB%AA%A9%EB%A1%9D

UPBIT_ERROR_CODE_MESSAGES = {
    "invalid_query_payload": "요청이 정상적으로 처리되지 않았어요. 다시 시도하거나 키를 다시 등록해주세요.",
    "jwt_verification": "키 인증에 실패했어요. 등록된 키가 정확한지 확인해주세요.",
    "expired_access_key": "등록된 API 키가 만료되었어요. Upbit에서 새 키를 발급받아 다시 등록해주세요.",
    "nonce_used": "요청이 중복되었어요. 페이지를 새로고침하고 다시 시도해주세요.",
    "no_authorization_ip": "현재 서버의 IP가 등록되어 있지 않아요. Upbit API 키 설정에서 IP 제한을 확인해주세요.",
    "out_of_scope": "등록된 키로는 이 기능을 사용할 수 없어요. API 키 권한을 다시 확인해주세요.",
}
