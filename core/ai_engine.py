import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

class AICore:
    def __init__(self):
        # Google AI Studio-дан алған API кілтті қолданамыз
        # Gemini-дің OpenAI-мен үйлесімді base_url-і осындай:
        self.client = AsyncOpenAI(
            api_key=os.getenv("GEMINI_API_KEY"),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        # Модель атауын Gemini-ге ауыстырамыз (мысалы: gemini-1.5-flash немесе gemini-1.5-pro)
        self.model = os.getenv("AI_MODEL", "gemini-1.5-flash")

    async def get_response(self, text: str):
        system_instruction = """
        Сенің есімің - Баяман. Сен қазақша сөйлейтін ақылды ассистентсің.
        Міндеттерің: сұраққа жауап беру, суретті сипаттау, фишингтен ескерту.
        Стилің: сыпайы, қысқа, "Мен Баяманмын" деп танысасың.
        """
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": text}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ Баяман (Gemini) қатесі: {str(e)}"

ai_engine = AICore()
