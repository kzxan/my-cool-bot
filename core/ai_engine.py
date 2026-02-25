import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

class AICore:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("AI_MODEL", "gpt-4-turbo")

    async def get_response(self, text: str):
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional assistant."},
                    {"role": "user", "content": text}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ AI Error: {str(e)}"

ai_engine = AICore()
