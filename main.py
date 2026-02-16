import asyncio
from aiogram import Bot, Dispatcher
from fastapi import FastAPI
from presentation.handlers.message import router as bot_router_message
from presentation.api.endpoints.save_message import router as api_router
from presentation.handlers.keyboards import router as bot_router_keyboards
import uvicorn
from infrastructure.config import settings

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()
dp.include_router(bot_router_message)
dp.include_router(bot_router_keyboards)

app = FastAPI()
app.include_router(api_router)


async def start_bot():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


async def start_server():
    config = uvicorn.Config(app, host="127.0.0.1", port=8000)
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    await asyncio.gather(start_bot(), start_server())


if __name__ == "__main__":
    asyncio.run(main())
