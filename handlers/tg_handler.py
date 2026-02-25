import os
from aiogram import Bot, Dispatcher, types
from core.ai_engine import ai_engine

bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
dp = Dispatcher()

@dp.message()
async def handle_tg(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    answer = await ai_engine.get_response(message.text)
    await message.reply(answer)