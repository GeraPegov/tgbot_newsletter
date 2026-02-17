from aiogram import Bot, Router, F
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
    InputMediaPhoto,
    InputMediaVideo,
    BufferedInputFile,
)
import aiohttp

send_out = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Отправить всем", callback_data="send_out")]
    ]
)

router = Router()


@router.callback_query(F.data == "send_out")
async def process_send_out(callback: CallbackQuery, bot: Bot):
    await callback.answer()
    user_id = callback.from_user.id

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"http://localhost:8000/message/records/{user_id}"
            ) as resp:
                messages = (await resp.json())["messages"]
            async with session.get("http://localhost:8000/message/users") as resp:
                users = (await resp.json())["users"]
    except aiohttp.ClientError:
        await bot.send_message(user_id, "Сервис недоступен")

    if not messages:
        await bot.send_message(user_id, "Нет данных")
        return

    for user in users:
        await send_to_user(bot, user, messages)


async def send_to_user(bot: Bot, user_id: int, messages: list):
    for file, file_type in messages:
        if file_type == "text":
            await bot.send_message(user_id, file)
            return

    media = []
    for file, file_type in messages:
        if file_type == "photo":
            media.append(InputMediaPhoto(media=file))
        elif file_type == "video":
            media.append(InputMediaVideo(media=file))

    if media:
        await bot.send_media_group(user_id, media)
