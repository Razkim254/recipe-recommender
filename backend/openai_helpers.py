# backend/openai_helpers.py
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def test_connection():
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # use a current model
        messages=[
            {"role": "user", "content": "Write a haiku about AI"}
        ],
        max_tokens=100
    )
    print(response.choices[0].message.content)

if __name__ == "__main__":
    test_connection()
