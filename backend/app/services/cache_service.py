import json, redis as redis_lib
from app.config import settings
_r = None
def get_redis():
    global _r
    if _r is None:
        try:
            _r = redis_lib.from_url(settings.REDIS_URL, decode_responses=True)
            _r.ping()
        except Exception:
            _r = None
    return _r
def cache_get(key):
    r = get_redis()
    if not r: return None
    try:
        v = r.get(key)
        return json.loads(v) if v else None
    except Exception:
        return None
def cache_set(key, value, ttl=3600):
    r = get_redis()
    if not r: return
    try:
        r.setex(key, ttl, json.dumps(value))
    except Exception:
        pass
def redis_health():
    r = get_redis()
    if not r: return "disconnected"
    try:
        r.ping()
        return "connected"
    except Exception:
        return "disconnected"
