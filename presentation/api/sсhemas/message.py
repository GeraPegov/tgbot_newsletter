from pydantic import BaseModel


class MessageModel(BaseModel):
    message: str
    user_id: int
    media_group_id: str | None
    message_type: str
