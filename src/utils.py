import os
import logfire
from pydantic_ai.usage import UsageLimits

LOGFIRE_TOKEN = os.getenv('LOGFIRE_TOKEN')
# 'if-token-present' means nothing will be sent (and the example will work) if you don't have logfire configured
logfire.configure(send_to_logfire=LOGFIRE_TOKEN)


usage_limits = UsageLimits(request_limit=15)
