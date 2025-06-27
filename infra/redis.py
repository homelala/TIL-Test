import logging
from contextlib import contextmanager
from redlock import RedLockFactory

factory = RedLockFactory(
    connection_details=[
        {"host": "localhost", "port": 6379, "db": 0},
        {"host": "localhost", "port": 6380, "db": 0},
        {"host": "localhost", "port": 6381, "db": 0},
    ]
)


@contextmanager
def create_lock(resource_key, ttl=5000):
    """
    분산 락 생성 및 해제
    :param resource_key: 락을 걸 Redis 키
    :param ttl: 락 유지 시간 (ms 단위)
    """
    lock = factory.create_lock(
        resource_key,
        ttl=ttl,
        retry_times=2,  # 락 재시도 횟수
        retry_delay=200,
    )

    if not lock.acquire():
        raise Exception(f"[LOCK] Unable to acquire lock for key: {resource_key}")

    try:
        print(f"🔒 락 획득 성공: {resource_key}")
        yield
    finally:
        lock.release()
        print(f"🔓 락 해제 완료: {resource_key}")

def create_order_redlock(product_id):
    return create_lock(RedLockKey.get_order_key(product_id))


class RedLockKey:
    @classmethod
    def get_order_key(cls, product_id):
        return f"Order:{product_id}"
