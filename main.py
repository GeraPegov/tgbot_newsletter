import asyncio
from aiogram import Bot, Dispatcher
from handlers import message

token = '8300080133:AAEdI4elJD_24r1qnkkIoXiZITFTlZE85c0'
TOKEN = token
bot = Bot(token=TOKEN)

dp = Dispatcher()

dp.include_router(message.router)

async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())