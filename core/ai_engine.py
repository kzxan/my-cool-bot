import os
import asyncio
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


class AICore:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")

        if not api_key:
            raise ValueError("GOOGLE_API_KEY табылмады")

        genai.configure(api_key=api_key)

        self.model = genai.GenerativeModel("gemini-1.5-flash")

    async def get_response(self, text: str):
        system_instruction = """
        Сенің есімің - Мэлс. Сен Мэлс есімді ақылды қазақша көмекшісің.
        
        1. Сәлемдесу: Пайдаланушы "Сәлем" немесе соған ұқсас амандасса ғана:
           "Сәлем! Мен Мэлспін, сіздің көмекшіңізбін. Қалай көмектесе аламын?" деп жауап бер.
        2. Нақты сұрақтар: Егер сұрақ нақты болса, өзіңді таныстырмай, бірден жауапқа көш.
        3. Фишингті анықтау: Хабарламада "ұтыс", "бонус", "шот бұғатталды",
           "карта мәліметі" немесе күмәнді сілтеме болса, бірден:
           "🚨 МЭЛС ЕСКЕРТЕДІ: Бұл фишингтік шабуыл болуы мүмкін!" деп дабыл қақ.
        4. Сурет салу: Пайдаланушы сурет сұраса, оның егжей-тегжейлі сипаттамасын (prompt) құрастырып бер.
        """

        try:
            full_prompt = f"{system_instruction}\n\nПайдаланушы: {text}"

            # Gemini SDK sync жұмыс істейді → async ету үшін thread қолданамыз
            response = await asyncio.to_thread(
                self.model.generate_content,
                full_prompt,
                generation_config={
                    "temperature": 0.7
                }
            )

            return response.text

        except Exception as e:
            return f"❌ Мэлс жүйесінде қате: {str(e)}"


ai_engine = AICore()
