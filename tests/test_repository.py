import pytest
from sqlalchemy import select
from infrastructure.models.message import UsersMessageModel
from infrastructure.repositories.message_repository import UsersMessageRepository


@pytest.mark.asyncio
async def test_save(async_session):
    repo = UsersMessageRepository(async_session)

    result = await repo.save(
        message="hello", user_id=2, media_group_id="2", message_type="str"
    )

    assert result is True


@pytest.mark.asyncio
async def test_check(async_session, test_message_postgres):
    repo = UsersMessageRepository(async_session)

    result = await repo._check(user_id=3, media_group_id="3")
    assert result is False

    result = await repo._check(user_id=1, media_group_id="1")
    assert result is True

    result = await repo._check(user_id=1, media_group_id=None)

    assert result is False


@pytest.mark.asyncio
async def test_delete(async_session, test_message_postgres):
    repo = UsersMessageRepository(async_session)
    await repo._delete(test_message_postgres.user_id)

    user = await async_session.execute(
        select(UsersMessageModel.id).where(
            UsersMessageModel.user_id == test_message_postgres.user_id
        )
    )

    assert user.scalar_one_or_none() is None


@pytest.mark.asyncio
async def test_get_users(async_session, test_message_postgres):
    repo = UsersMessageRepository(async_session)

    users = await repo.get_users()
    assert users[0] == test_message_postgres.user_id

    await repo._delete(test_message_postgres.user_id)
    users = await repo.get_users()

    assert users is None


@pytest.mark.asyncio
async def test_get_message(async_session, test_message_postgres):
    repo = UsersMessageRepository(async_session)

    message = await repo.get_messages(test_message_postgres.user_id)

    assert message[0][0] == test_message_postgres.message
    assert message[0][1] == test_message_postgres.message_type
