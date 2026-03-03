import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

class AICore:
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=os.getenv("GEMINI_API_KEY"),
            # 'v1' орнына 'v1beta' қолдану маңызды
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        # Кейбір жағдайда 'models/gemini-1.5-flash' деп толық жазу керек болуы мүмкін
        self.model = os.getenv("AI_MODEL", "gemini-1.5-flash")

    async def get_response(self, text: str):
        # Мэлстің ішкі нұсқаулығы
        system_instruction = """
        Сенің есімің - Мэлс. Сен қазақ тілді өте ақылды әрі қауіпсіздік сарапшысы ассистентсің.
        
        Жауап беру ережелері:
        1. Сәлемдесу: Егер пайдаланушы тек "Сәлем", "Привет", "Қайырлы күн" сияқты амандасу сөздерін жазса ғана: "Сәлем! Мен Мэлспін, сіздің көмекшіңізбін. Қалай көмектесе аламын?" деп жауап бер.
        2. Басқа сұрақтар: Егер пайдаланушы нақты сұрақ қойса немесе тапсырма берсе, өзіңді таныстырмай, бірден іске көш. Артық сөз жазба.
        3. Фишингті тану (Өте маңызды): Пайдаланушы жіберген мәтінде немесе сілтемеде алаяқтық белгілері болса (мысалы: "Kaspi ұтыс", "акция", "сілтемеге өт", "тегін ақша", "карта мәліметін енгіз"), бірден мына фразамен баста: "🚨 МЭЛС ЕСКЕРТЕДІ: Бұл фишингтік шабуыл немесе алаяқтық болуы мүмкін! Сақ болыңыз." сосын себебін түсіндір.
        4. Сурет салу: Сурет сұраса, оны кәсіби деңгейде сипаттап бер (prompt жаса).
        """
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": text}
                ],
                temperature=0.5
            )
            return response.choices[0].message.content
        except Exception as e:
            # Егер қате қайталанса, модель атын "models/gemini-1.5-flash" деп көріңіз
            return f"❌ Мэлс жүйесінде қате: {str(e)}"

ai_engine = AICore()
