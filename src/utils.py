from concurrent.futures import ThreadPoolExecutor
import dotenv
from functools import wraps
import time
import os
import logfire
from pydantic_ai.usage import UsageLimits
from tqdm import tqdm
dotenv.load_dotenv()

LOGFIRE_TOKEN = os.getenv('LOGFIRE_TOKEN')

logfire.configure(send_to_logfire=LOGFIRE_TOKEN)

usage_limits = UsageLimits(request_limit=15)


def exponential_retry(retries, return_value_if_fail=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    if attempt >= retries:
                        logfire.error(
                            f"Function {func.__name__} failed after {attempt} attempts: {e}")
                        return return_value_if_fail
                    sleep_time = 2 ** attempt  # Exponential backoff
                    time.sleep(sleep_time)
        return wrapper
    return decorator


def multi_threading(function, parameters, max_workers=5, desc=""):
    pbar = tqdm(total=len(parameters), desc=desc, leave=True, position=0)
    event = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # not need chucksize
        for result in executor.map(function, parameters):
            event.append(result)
            pbar.update(1)
    pbar.close()

    return event
