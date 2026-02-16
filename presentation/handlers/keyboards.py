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
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=f"http://localhost:8000/message/records/{user_id}"
        ) as resp:
            data = (await resp.json())["records"]

        async with session.get(url="http://localhost:8000/message/users") as resp:
            users = (await resp.json())["users"]

    media = []
    for list_out in data:
        file, file_type = list_out
        if file_type == "text":
            media = file
            break
        elif file_type == "photo":
            media.append(InputMediaPhoto(media=file))
        elif file_type == "video":
            media.append(InputMediaVideo(media=file))

    if isinstance(media, list):
        for user in users:
            await bot.send_media_group(user, media)
    elif isinstance(media, str):
        for user in users:
            await bot.send_message(user, media)
