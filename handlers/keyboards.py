
from operator import call
from aiogram import Bot, Router, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InputMediaPhoto, InputMediaVideo, BufferedInputFile
from fastapi import Depends

from dependencies.get_message_service import get_message_service
from services.message_service import UsersMessageService


send_out = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Отправить всем', callback_data='send')]
    ])

router = Router()

@router.callback_query(F.data == "send_out")
async def process_send_out(
    callback: CallbackQuery,
    bot: Bot,
    message_service: UsersMessageService = Depends(get_message_service)
    ):
    user_id = callback.from_user.id
    data = await message_service.get_messages(user_id)

    if isinstance(data, list):
        media = []
        for tuple_out in data:
            file, file_type = tuple_out
            if file_type == 'photo':
                media.append(InputMediaPhoto(media=BufferedInputFile(file, 'photo.jpg')))
            elif file_type == 'video':
                media.append(InputMediaVideo(media=BufferedInputFile(file, 'video.mp4')))
        await bot.send_media_group(callback.message.chat.id, media)
    else:
        await callback.answer()
        await callback.message.answer(data)
