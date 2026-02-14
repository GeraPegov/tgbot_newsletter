from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.models.message import UsersMessageModel

class UsersMessageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    
    async def save(self, messages, user_id):
        objects = [UsersMessageModel(
                user_id=user_id,
                message_bytes=bytes(message)
            ) for message in messages]

        self.session.add_all(objects)

        await self.session.commit()

        return True

    async def get_message(self, user_id: int):
        messages = await self.session.execute(
            select(UsersMessageModel)
            .where(UsersMessageModel.user_id==user_id)
        )
        message = messages.scalars().all()
        return messages if len(message) > 0 else None