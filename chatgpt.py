import asyncio
import time

import openai

# Rate limit for free users
RATE_LIMIT: int = 3  # 3 requests per minute

# Variables to track rate limit
request_count: int = 0
last_request_time: float = 0

async def generate_explanation(prompt: str, api_key: str) -> str:
    """
    Generates a response from the ChatGPT model based on a given prompt.

    Args:
        prompt (str): The prompt for generating the response.
        api_key (str): The API key.

    Returns:
        str: The generated response from the ChatGPT model.
    """
    global request_count, last_request_time

    # Check rate limit
    current_time: float = time.time()
    time_elapsed: float = current_time - last_request_time

    if time_elapsed < 60 and request_count >= RATE_LIMIT:
        await asyncio.sleep(60 - time_elapsed)
        request_count = 0
        last_request_time = current_time

    openai.api_key = api_key
    response = await asyncio.to_thread(openai.ChatCompletion.create,
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
    )

    request_count += 1
    last_request_time = time.time()

    if 'choices' in response:
        return response['choices'][0]['message']['content'].strip()
    return ""
