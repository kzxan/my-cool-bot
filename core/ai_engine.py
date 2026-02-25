import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

# .env файлынан айнымалыларды жүктеу
load_dotenv()

class AICore:
    def __init__(self):
        # Groq API-ге қосылу үшін base_url міндетті түрде көрсетіледі
        self.client = AsyncOpenAI(
            api_key=os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        )
        # Модельді .env файлынан алады немесе llama-3.3-70b-versatile қолданады
        self.model = os.getenv("AI_MODEL", "llama-3.3-70b-versatile")

    async def get_response(self, text: str):
        # Алаяқтықты тануға арналған кеңейтілген System Prompt
        system_instruction = """
        Сіз - Қазақстандағы киберқауіпсіздік және алаяқтыққа қарсы күрес (Anti-Fraud) маманысыз.
        Сіздің міндетіңіз - пайдаланушы жіберген хабарламадағы алаяқтық белгілерін анықтау.

        МЫНА "ҚЫЗЫЛ ЖАЛАУШАЛАРДЫ" ІЗДЕҢІЗ:
        1. БАНКТЕР (Kaspi, Halyk т.б.): "Қауіпсіз шот", "транзакцияны тоқтату", "СМС-кодты немесе ПИН-кодты айту".
        2. ЖАЛҒАН ИНВЕСТИЦИЯ: "ҚазМұнайГаз", "Halyk" немесе "Air Astana" атынан тез арада табыс табу ұсыныстары.
        3. ЖЕТКІЗУ (OLX, Казпочта): "Ақшаны алу үшін мына сілтемеге өтіп, карта мәліметтерін (CVV) жаз".
        4. МЕМЛЕКЕТТІК ОРГАНДАР: "Полициядан немесе ҰҚК-ден хабарласып тұрмыз, сіз қылмысқа қатыстысыз, ақша аударыңыз".
        5. ЖҰМЫС: "Күніне 20-50 мың теңге табыс, тек сілтемелерге басу керек, бірақ алдын ала жарна төле".

        ЖАУАП БЕРУ ФОРМАТЫ:
        - ҚАУІП ДЕҢГЕЙІ: (Төмен / Орташа / Жоғары)
        - АНЫҚТАЛҒАН ТӘСІЛ: (Мысалы: Фишинг немесе Әлеуметтік инженерия)
        - ТҮСІНДІРМЕ: Неге бұл күмәнді?
        - КЕҢЕС: Пайдаланушы не істеуі керек?

        Тек қазақ тілінде, қысқа әрі нақты жауап беріңіз.
        """

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": f"Мына мәтінді алаяқтыққа талда: {text}"}
                ],
                temperature=0.2 # Нақтылықты сақтау үшін төмен температура
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ AI Error: {str(e)}"

# Класты инициализациялау
ai_engine = AICore()
