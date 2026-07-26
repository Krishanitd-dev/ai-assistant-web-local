from openai import OpenAI
from config import GROQ_API_KEY
from app.prompts import AI_SYSTEM_PROMPT

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

MODEL = "llama-3.3-70b-versatile"


def get_ai_response(question):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
                {
                "role": "system",
                "content": AI_SYSTEM_PROMPT},
                { 
                "role": "user",
                "content": question
                }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content