from sqlalchemy import BigInteger, Integer, String
from infrastructure.connection_postgres import Base
from sqlalchemy.orm import Mapped, mapped_column


class UsersMessageModel(Base):
    __tablename__ = "users_message"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    media_group_id: Mapped[str | None] = mapped_column(String, nullable=True)
    message: Mapped[str] = mapped_column(String)
    message_type: Mapped[str] = mapped_column(String)
