import time
from functools import wraps

def retry(times=3, delay=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"[Retry] Attempt {attempt} failed → {e}")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator
