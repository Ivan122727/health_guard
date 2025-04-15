from shared.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from shared.sqlalchemy_db_.sqlalchemy_model import UserDBM


async def main():
    with get_cached_sqlalchemy_db().new_session() as session:
        user = UserDBM(
            tg_id=123,
        )
        session.add(user)
        session.commit()
        session.refresh(user)
    print(user)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())