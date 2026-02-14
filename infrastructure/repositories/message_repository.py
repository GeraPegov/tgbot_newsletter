from sqlalchemy import and_, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.models.message import UsersMessageModel

class UsersMessageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _check(self, user_id: int, media_group_id: str):
        user = await self.session.execute(
            select(UsersMessageModel.id)
            .where(and_(UsersMessageModel.user_id==user_id,
                   UsersMessageModel.media_group_id==media_group_id))
        )
        check_live = user.scalar_one_or_none()

        return True if check_live else False
    
    async def _delete(self, user_id: int):
        await self.session.execute(
            delete(UsersMessageModel)
            .where(UsersMessageModel.user_id==user_id)
        )

    async def _type(self, message):
        pass

    async def save(
            self,
            message: str,
            user_id: int,
            media_group_id: str,
            message_type: str
            ):
        check_records = await self._check(user_id, media_group_id)
        if check_records is False:
            await self._delete(user_id)

        objects = UsersMessageModel(
                user_id=user_id,
                message_bytes=message.encode('utf-8') if isinstance(message, str) else message,
                media_group_id=media_group_id,
                message_type=message_type
        )
        self.session.add(objects)
        await self.session.commit()
        return True

    async def get_message(self, user_id: int):
        messages = await self.session.execute(
            select(
                UsersMessageModel.message_bytes,
                UsersMessageModel.message_type
                )
            .where(UsersMessageModel.user_id==user_id)
        )
        records = messages.scalars().all()
        if records[0][1] == 'text':
            return records[0][1].decode('utf-8')
        return records


