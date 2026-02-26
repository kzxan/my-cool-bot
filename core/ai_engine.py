import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

class AICore:
    def __init__(self):
        # Groq-ты қолданамыз
        self.client = AsyncOpenAI(
            api_key=os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        )
        self.model = os.getenv("AI_MODEL", "llama-3.3-70b-versatile")

    async def get_response(self, text: str):
        # Баяманның "тұлғасы" мен мультимедиа нұсқаулығы
        system_instruction = """
        Сенің есімің - Баяман. Сен Meta AI сияқты ақылды, достық ниеттегі қазақша виртуалды ассистентсің.
        
        Сенің басты міндеттерің:
        1. Кез келген сұраққа жауап беру (Meta AI сияқты).
        2. Сурет салу (Image Generation): Егер пайдаланушы сурет сұраса, оған суреттің толық сипаттамасын (prompt) құрастырып, оны қалай елестететініңді айт.
        3. Музыка мен Видео: Олардың сценарийін, сөзін немесе құрылымын жасап бер.
        4. Фишингті анықтау: Егер хабарламада алаяқтық белгілері болса, бірден "Баяман ескертеді: Бұл қауіпті!" деп дабыл қақ.
        
        Сөйлеу стилі:
        - Әрдайым "Мен Баяманмын" немесе "Менің атым Баяман" деп таныстыра аласың.
        - Сөзің сыпайы, ақылды әрі қысқа болсын.
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
            return f"❌ Баяман қатесі: {str(e)}"

ai_engine = AICore()
