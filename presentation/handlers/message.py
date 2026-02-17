from aiogram import Router, F
from aiogram.types import Message
import aiohttp
from presentation.handlers.keyboards import send_out

router = Router()
processed_media_groups = set()


@router.message(F.photo)
async def get_photo(message: Message, message_type="photo"):
    file_id = message.photo[-1].file_id
    user_id = message.from_user.id
    media_group_id = message.media_group_id

    try:
        async with aiohttp.ClientSession() as session:
            await session.post(
                "http://localhost:8000/message/save",
                json={
                    "message": file_id,
                    "user_id": user_id,
                    "media_group_id": media_group_id,
                    "message_type": message_type,
                },
            )
    except aiohttp.ClientError:
        await message.answer("Сервис недоступен")
        return

    if media_group_id is None or media_group_id not in processed_media_groups:
        if media_group_id:
            processed_media_groups.add(media_group_id)
        await message.answer("Рассылка", reply_markup=send_out)


@router.message(F.text)
async def get_text(message: Message, message_type: str = "text"):
    text = message.text
    user_id = message.from_user.id
    media_group_id = message.media_group_id

    try:
        async with aiohttp.ClientSession() as session:
            await session.post(
                "http://localhost:8000/message/save",
                json={
                    "message": text,
                    "user_id": user_id,
                    "media_group_id": media_group_id,
                    "message_type": message_type,
                },
            )
    except aiohttp.ClientError:
        await message.answer("Сервис недоступен")

    await message.answer("Рассылка", reply_markup=send_out)


@router.message(F.video)
async def get_video(message: Message, message_type: str = "video"):
    file_id = message.video.file_id
    user_id = message.from_user.id
    media_group_id = message.media_group_id

    try:
        async with aiohttp.ClientSession() as session:
            await session.post(
                "http://localhost:8000/message/save",
                json={
                    "message": file_id,
                    "user_id": user_id,
                    "media_group_id": media_group_id,
                    "message_type": message_type,
                },
            )
    except aiohttp.ClientError:
        await message.answer("Сервис недоступен")
        return

    if media_group_id is None or media_group_id not in processed_media_groups:
        if media_group_id:
            processed_media_groups.add(media_group_id)
        await message.answer("Рассылка", reply_markup=send_out)
