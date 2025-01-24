from openai import OpenAI
import pandas as pd
from typing import Tuple
from dotenv import load_dotenv
import time
import os
from tenacity import retry, stop_after_attempt, wait_exponential

# Load environment variables
load_dotenv()

# Initialize OpenAI API
openai = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key='yourkey' # Ensure API key is loaded securely
)

# Define sentiment analysis function using OpenAI API
@retry(
    wait=wait_exponential(multiplier=1, min=4, max=60),  
    stop=stop_after_attempt(3)  
)
def analyze_sentiment(text: str) -> Tuple[str, float]:
    try:
        time.sleep(10)  # Introducing a delay to prevent hitting API limits

        # Request to the OpenAI API for sentiment analysis
        completion = openai.chat.completions.create(
            model="google/gemini-2.0-flash-exp:free",  # Specify your model name
            messages=[
                {
                    "role": "system",
                    "content": "You are a sentiment analysis expert. Analyze the sentiment of the given text and respond with only: sentiment_label (positive, negative, or neutral)."
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )
        
        # Extract sentiment prediction from API response
        pred_sent = completion.choices[0].message.content.strip()
        return pred_sent
    except Exception as e:
        print(f"Error analyzing sentiment for text: {e}")
        raise  # Retry will occur if there’s an exception
