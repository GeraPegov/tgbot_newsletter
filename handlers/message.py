
from io import BytesIO
from aiogram import Bot, Router, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from fastapi import Depends

from dependencies.get_message_service import get_message_service
from services.message_service import UsersMessageService
from handlers.keyboards import send_out

router = Router()

@router.message(F.photo)
async def get_photo(
    message: Message,
    bot: Bot,
    message_type = 'photo',
    ):
    message_service: UsersMessageService = get_message_service()

    file_id = message.photo[-1].file_id
    photo_bytes = await message_service.download_file(file_id, bot)
    user_id = message.from_user.id
    media_group_id = message.media_group_id

    await message_service.save_messages(
        message=photo_bytes,
        user_id=user_id,
        message_type=message_type,
        media_group_id=media_group_id
    )

    await message.answer('Рассылка', reply_markup=send_out)

    

# @router.message(F.text)
# async def get_text(
#     message: Message,
#     message_service: UsersMessageService = Depends(get_message_service)
#     ):
#     user_id = message.from_user.id
#     text = message.text
#     media_group_id = message.media_group_id

#     save = message_service.save_messages(text, user_id, media_group_id)


# @router.message(F.video)
# async def get_video(message: Message):
#     pass

# @router.message(F.photo)
# async def get(message: Message):
#     # objects = []
#     # objects.append(message.photo[0].file_id)
#     # print(objects)
#     print(message.media_group_id)


