from nameko.rpc import rpc
import redis


class RedisSyncServiceX:
    name = "sync_redis_x"

    def __init__(self) -> None:
        self.redis_db = None

    @rpc
    def process_data(self):
        self.redis_db = redis.Redis(host='redis', port=6379, db=0)
        processed_data = ''
        for key in self.redis_db.scan_iter():
            value = self.redis_db.get(key)
            processed_data += f'Key: {key}, Value: {value}\n'
        return processed_data