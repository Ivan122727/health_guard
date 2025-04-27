from datetime import datetime
import os
from pathlib import Path
import sys

import pytz

# Получаем путь к родительской директории
parent_dir = Path(__file__).parent.parent
# Добавляем родительскую директорию в PYTHONPATH
sys.path.append(str(parent_dir))
# Устанавливаем текущую рабочую директорию
os.chdir(parent_dir)

from shared.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from shared.sqlalchemy_db_.sqlalchemy_model import UserDBM, SurveyDBM, DoctorPatientDBM, SurveyQuestionDBM, QuestionDBM

async def make_test_data():
    get_cached_sqlalchemy_db().reinit()

    async with get_cached_sqlalchemy_db().new_async_session() as async_session:

        doctor_dbm = UserDBM(
            tg_id=380138374,
            role=UserDBM.Roles.doctor,
            full_name="Шакирзянов  Айдар  Анварович"
        )
        async_session.add(doctor_dbm)
        await async_session.flush()

        doctor_dbm = UserDBM(
            tg_id=457643251,
            role=UserDBM.Roles.doctor,
            full_name="Ермолов  Иван  Олегович",
        )
        async_session.add(doctor_dbm)
        await async_session.flush()
        await async_session.refresh(doctor_dbm)

        for i in range(1, 20):
            patient_dbm = UserDBM(
                tg_id=457643251 + i,
                role=UserDBM.Roles.patient,
                full_name=f"Ермолов  Иван  Олегович {i}"
            )
            async_session.add(patient_dbm)
            await async_session.flush()
            await async_session.refresh(patient_dbm)

            doctor_patient = DoctorPatientDBM(
                doctor=doctor_dbm,
                patient=patient_dbm,
            )
            async_session.add(doctor_patient)
            await async_session.flush()
        
        question_dbms: list[QuestionDBM] = []
        
        question_dbm = QuestionDBM(
            created_by=doctor_dbm.tg_id,
            question_text="Как часто вы испытываете головную боль?",
            question_type=QuestionDBM.QuestionType.CHOICE,
            answer_options=["Никогда", "Редко (1-2 раза в месяц)", "Иногда (1-2 раза в неделю)", "Часто (3-5 раз в неделю)", "Постоянно"],
            is_public=True,
        )
        async_session.add(question_dbm)
        await async_session.flush()
        await async_session.refresh(question_dbm)
        question_dbms.append(question_dbm)

        question_dbm = QuestionDBM(
            created_by=doctor_dbm.tg_id,
            question_text="Оцените качество сна по шкале от 1 до 5",
            question_type=QuestionDBM.QuestionType.CHOICE,
            answer_options=["1", "2", "3", "4", "5"],
            is_public=True,
        )
        async_session.add(question_dbm)
        await async_session.flush()
        await async_session.refresh(question_dbm)
        question_dbms.append(question_dbm)


        question_dbm = QuestionDBM(
            created_by=doctor_dbm.tg_id,
            question_text="Какие лекарства вы принимаете регулярно?",
            question_type=QuestionDBM.QuestionType.CHOICE,
            answer_options=["Никакие", "Телзап", "Беталок"],
            is_public=True,
        )
        async_session.add(question_dbm)
        await async_session.flush()
        await async_session.refresh(question_dbm)
        question_dbms.append(question_dbm)

        survey_dbm = SurveyDBM(
            title="Оценка состояния здоровья",
            created_by=doctor_dbm.tg_id,
        )
        
        async_session.add(survey_dbm)
        await async_session.flush()
        await async_session.refresh(survey_dbm)

        order_index = 1
        for question_dbm in question_dbms:
            survey_question = SurveyQuestionDBM(
                survey_id=survey_dbm.id,
                question_id=question_dbm.id,
                order_index=order_index,
            )
            async_session.add(survey_question)
            await async_session.flush()
            
            order_index += 1

        await async_session.commit()

if __name__ == "__main__":
    import asyncio
    asyncio.run(make_test_data())