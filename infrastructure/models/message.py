from sqlalchemy import Integer, LargeBinary, String
from infrastructure.connection_postgres import Base
from sqlalchemy.orm import Mapped, mapped_column

class UsersMessageModel(Base):
    __tablename__ = 'users_message'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer)
    message_bytes: Mapped[bytes | None] = mapped_column(LargeBinary)
    message_id: Mapped[str | None] = mapped_column(String)
