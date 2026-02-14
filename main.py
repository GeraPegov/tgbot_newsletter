import asyncio
from aiogram import Bot, Dispatcher
from handlers import message
from aiogram.client.session.aiohttp import AiohttpSession
import aiohttp

token = '8300080133:AAEdI4elJD_24r1qnkkIoXiZITFTlZE85c0'
TOKEN = token

bot = Bot(token=TOKEN)
# session = AiohttpSession(
#     timeout=aiohttp.ClientTimeout(total=60)
# )

# bot.session.timeout = 60
dp = Dispatcher()

dp.include_router(message.router)


async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())