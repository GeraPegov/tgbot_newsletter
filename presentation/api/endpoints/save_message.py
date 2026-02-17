from fastapi import Depends
from fastapi.routing import APIRouter

from presentation.api.sсhemas.message import MessageModel
from presentation.dependencies.get_message_service import get_message_service
from services.message_service import UsersMessageService

router = APIRouter()


@router.post("/message/save")
async def save(
    message_from_bot: MessageModel,
    message_service: UsersMessageService = Depends(get_message_service),
):
    await message_service.save_message(
        message=message_from_bot.message,
        user_id=message_from_bot.user_id,
        media_group_id=message_from_bot.media_group_id,
        message_type=message_from_bot.message_type,
    )
    return {"status": "okay"}


@router.get("/message/records/{user_id}")
async def records(
    user_id: int, message_service: UsersMessageService = Depends(get_message_service)
):
    messages = await message_service.get_messages(user_id)
    return {"messages": messages}


@router.get("/message/users")
async def users(message_service: UsersMessageService = Depends(get_message_service)):
    users = await message_service.get_users()
    return {"users": users}
