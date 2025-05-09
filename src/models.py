import os
from httpx import AsyncClient
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.deepseek import DeepSeekProvider

DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')

custom_http_client = AsyncClient(timeout=30)
model = OpenAIModel(
    'deepseek-chat',
    provider=DeepSeekProvider(
        api_key=DEEPSEEK_API_KEY,
        http_client=custom_http_client
    ),
)
