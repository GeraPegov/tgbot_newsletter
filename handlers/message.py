
from aiogram import Router, F
from aiogram.types import Message
from fastapi import Depends

from dependencies.get_message_service import get_message_service
from services.message_service import UsersMessageService

router = Router()

# @router.message(F.photo)
# async def get_photo(message: Message):
#     id_photo = message.photo[0].file_id

# @router.message(F.text)
# async def get_text(
#     message: Message,
#     message_service: MessageService = Depends(get_message_service)
#     ):
#     user_id = message.from_user.id
#     text = message.text
#     in_repo = message_service.save(text, user_id)


# @router.message(F.video)
# async def get_video(message: Message):
#     pass

@router.message(F.photo)
async def get(message: Message):
    # objects = []
    # objects.append(message.photo[0].file_id)
    # print(objects)
    print(message.media_group_id)

