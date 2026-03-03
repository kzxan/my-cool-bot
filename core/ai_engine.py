import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

class AICore:
    def __init__(self):
        # API кілтті алу
        api_key = os.getenv("GEMINI_API_KEY")
        
        self.client = AsyncOpenAI(
            api_key=api_key,
            # 'v1beta' нұсқасын қолдану 404 қатесін жояды
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        # Кейбір жүйелерде "models/gemini-1.5-flash" деп толық жазу қажет болуы мүмкін
        self.model = "gemini-1.5-flash"

    async def get_response(self, text: str):
        # Мэлстің тұлғасы мен фишингті тану логикасы
        system_instruction = """
        Сенің есімің - Мэлс. Сен Мэлс есімді ақылды қазақша көмекшісің.
        
        1. Сәлемдесу: Пайдаланушы "Сәлем" немесе соған ұқсас амандасса ғана: "Сәлем! Мен Мэлспін, сіздің көмекшіңізбін. Қалай көмектесе аламын?" деп жауап бер.
        2. Нақты сұрақтар: Егер сұрақ нақты болса, өзіңді таныстырмай, бірден жауапқа көш.
        3. Фишингті анықтау: Хабарламада "ұтыс", "бонус", "шот бұғатталды", "карта мәліметі" немесе күмәнді сілтеме болса, бірден: "🚨 МЭЛС ЕСКЕРТЕДІ: Бұл фишингтік шабуыл болуы мүмкін!" деп дабыл қақ.
        4. Сурет салу: Пайдаланушы сурет сұраса, оның егжей-тегжейлі сипаттамасын (prompt) құрастырып бер.
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
            # Егер тағы да 404 берсе, модель есімін 'models/gemini-1.5-flash' деп өзгертіп көріңіз
            return f"❌ Мэлс жүйесінде қате: {str(e)}"

ai_engine = AICore()
