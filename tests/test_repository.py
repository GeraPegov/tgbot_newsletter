
import pytest
from sqlalchemy import select
from infrastructure.models.message import UsersMessageModel
from infrastructure.repositories.message_repository import UsersMessageRepository


@pytest.mark.asyncio
async def test_save(async_session):
    repo = UsersMessageRepository(async_session)

    result = await repo.save(
        message='hello',
        user_id=2,
        media_group_id='2',
        message_type='str'
    )

    assert result is True

@pytest.mark.asyncio
async def test_check(async_session, test_record):
    repo = UsersMessageRepository(async_session)

    result = await repo._check(
        user_id=3,
        media_group_id='3'
        )
    assert result is False

    result = await repo._check(
        user_id=1,
        media_group_id='1'
    )
    assert result is True

    result = await repo._check(
        user_id=1,
        media_group_id=None
    )

    assert result is False

@pytest.mark.asyncio
async def test_delete(async_session, test_record):
    repo = UsersMessageRepository(async_session)
    await repo._delete(test_record.user_id)

    user = await async_session.execute(
        select(UsersMessageModel.id)
        .where(UsersMessageModel.user_id==test_record.user_id)
    )

    assert user.scalar_one_or_none() is None








