import json
from typing import Any, Callable

import redis
from django.conf import settings


# 전역 Redis 클라이언트
cache = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)


def get_or_set_cache(key: str, ttl: int, compute_fn: Callable[[], Any]) -> Any:
    """
    Redis 캐시에서 데이터를 가져오거나, 없을 경우 compute_fn을 실행하여 저장 후 반환합니다.

    :param key: Redis에 저장될 키
    :param ttl: 캐시 유지 시간 (초 단위)
    :param compute_fn: 캐시되지 않은 경우 호출할 함수
    :return: 캐시된 값 또는 새로 계산된 값
    """
    try:
        cached = cache.get(key)
        if cached is not None:
            return json.loads(cached)
    except (redis.RedisError, json.JSONDecodeError):
        pass  # 캐시 조회 실패 시 무시하고 새로 계산

    result = compute_fn()

    try:
        cache.setex(key, ttl, json.dumps(result))
    except redis.RedisError:
        pass  # 저장 실패 시에도 결과는 반환

    return result
