import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

class AICore:
    def __init__(self):  # _init_ емес, қос астын сызу __init__ болуы керек
        # Groq-тың ресми base_url-і қосылды
        self.client = AsyncOpenAI(
            api_key=os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        )
        # Модельді Groq-тың тегін моделіне ауыстырамыз (llama-3.3-70b-versatile)
        self.model = os.getenv("AI_MODEL", "llama-3.3-70b-versatile")

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
