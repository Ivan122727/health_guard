from shared.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from shared.sqlalchemy_db_.sqlalchemy_model import UserDBM, DoctorPatient, QuestionDBM
import sqlalchemy
from sqlalchemy.orm import joinedload

async def main():
    get_cached_sqlalchemy_db().reinit()
    
    # Создаем доктора
    async with get_cached_sqlalchemy_db().new_async_session() as async_session:
        doctor = UserDBM(
            tg_id=12345,
            role=UserDBM.Roles.patient
        )
        async_session.add(doctor)
        await async_session.commit()
        await async_session.refresh(doctor)
        
    print(doctor)

    

    # Создаем вопрос
    async with get_cached_sqlalchemy_db().new_async_session() as async_session:
        question = QuestionDBM( 
            question_text="Как вы себя чувствуете?",
            question_type=QuestionDBM.QuestionType.TEXT,
            created_by=doctor.id
        )
        
        async_session.add(question)
        await async_session.commit()
        await async_session.refresh(question)

        question = (await async_session.execute(
                sqlalchemy
                .select(QuestionDBM)
                .filter(QuestionDBM.id == question.id)
                .options(joinedload(QuestionDBM.author))
        )).scalars().one()


        
    print(question)
    print(question.author)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())