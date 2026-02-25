import asyncio
import uvicorn
from fastapi import FastAPI
from handlers.tg_handler import bot, dp
from handlers.wa_handler import router as wa_router

app = FastAPI()
app.include_router(wa_router)

async def run_tg():
    print("🚀 Telegram bot started...")
    await dp.start_polling(bot)

async def run_wa():
    print("📱 WhatsApp Webhook server started...")
    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    # Запускаем оба сервиса параллельно
    await asyncio.gather(run_tg(), run_wa())

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("STOPPED")