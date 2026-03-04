import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

class AICore:
    def __init__(self):
        # Groq-ты қолданамыз - бұл қазіргі ең тұрақты нұсқа
        self.client = AsyncOpenAI(
            api_key=os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        )
        # Ең мықты модельдердің бірі
        self.model = "llama-3.3-70b-versatile"

    async def get_response(self, text: str):
        # Мэлстің баптаулары
        system_instruction = """
        Сенің есімің - Мэлс. Сен өте ақылды қазақша көмекшісің.
        
        Тәртібің:
        1. Сәлемдесу: Пайдаланушы "сәлем" десе: "Сәлем! Мен Мэлспін, сіздің көмекшіңізбін. Қалай көмектесе аламын?" деп қана жауап бер.
        2. Басқа сұрақтар: Бірден іске көш, өзіңді таныстырма.
        3. Фишинг: Мәтінде алаяқтық (банк, ұтыс, күмәнді сілтеме) болса, бірден: "🚨 МЭЛС ЕСКЕРТЕДІ: Бұл фишингтік шабуыл болуы мүмкін!" деп жауап бер.
        4. Сурет салу: Пайдаланушы сурет сұраса, оған кәсіби промпт (сипаттама) жазып бер.
        """
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": text}
                ],
                temperature=0.6
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ Мэлс (Groq) қатесі: {str(e)}"

ai_engine = AICore()
