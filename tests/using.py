from datetime import datetime, timedelta, timezone
from shared.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from shared.sqlalchemy_db_.sqlalchemy_model import (
    UserDBM, 
    QuestionDBM, 
    SurveyDBM, 
    SurveyQuestionDBM,
    ScheduledSurveyDBM,
    SurveyReminderDBM,
    SurveyResponseDBM
)
import asyncio
import json

async def main():
    db = get_cached_sqlalchemy_db()
    db.reinit()
    
    async with db.new_async_session() as session:
        try:
            # 1. Создаем доктора
            doctor = UserDBM(
                tg_id=12345,
                role=UserDBM.Roles.doctor
            )
            session.add(doctor)
            await session.flush()
            print(f"Создан доктор (id={doctor.id}, tg_id={doctor.tg_id})")

            # 2. Создаем пациента
            patient = UserDBM(
                tg_id=54321,
                role=UserDBM.Roles.patient,
                full_name="Иванов Иван Иванович"
            )
            session.add(patient)
            await session.flush()
            print(f"Создан пациент (id={patient.id}, ФИО={patient.full_name})")

            # 3. Создаем вопрос
            question = QuestionDBM(
                question_text="Как вы себя чувствуете сегодня?",
                question_type=QuestionDBM.QuestionType.CHOICE,
                created_by=doctor.id,
                answer_options=["Хорошо", "Плохо", "Отлично"]
            )
            session.add(question)
            await session.flush()
            print(f"Создан вопрос (id={question.id})")

            # 4. Создаем опрос
            survey = SurveyDBM(
                title="Ежедневный опрос о самочувствии",
                created_by=doctor.id
            )
            session.add(survey)
            await session.flush()
            print(f"Создан опрос (id={survey.id})")

            # 5. Связываем опрос с вопросом
            survey_question = SurveyQuestionDBM(
                survey_id=survey.id,
                question_id=question.id,
                order_index=1
            )
            session.add(survey_question)
            await session.flush()
            print(f"Добавлен вопрос в опрос (порядок={survey_question.order_index})")

            # 6. Создаем запланированный опрос для пациента
            now = datetime.now(timezone.utc)
            scheduled_survey = ScheduledSurveyDBM(
                survey_id=survey.id,
                patient_id=patient.id,
                doctor_id=doctor.id,
                frequency_type="daily",
                times_per_day=2,
                start_date=now.replace(tzinfo=None),
                end_date=(now + timedelta(days=7)).replace(tzinfo=None),
                max_reminders=3,
                reminder_interval_hours=2,
                is_active=True,
                next_scheduled_time=(now + timedelta(hours=1)).replace(tzinfo=None)
            )
            session.add(scheduled_survey)
            await session.flush()
            
            # 7. Создаем напоминания для запланированного опроса
            reminder_data = []
            for i in range(1, scheduled_survey.max_reminders + 1):
                reminder_time = scheduled_survey.next_scheduled_time + timedelta(
                    hours=(i-1)*scheduled_survey.reminder_interval_hours
                )
                
                reminder = SurveyReminderDBM(
                    scheduled_survey_id=scheduled_survey.id,
                    reminder_number=i,
                    scheduled_time=reminder_time,
                    status=SurveyReminderDBM.ReminderStatus.PENDING
                )
                session.add(reminder)
                await session.flush()
                
                reminder_data.append({
                    'id': reminder.id,
                    'number': i,
                    'time': reminder_time,
                    'status': 'pending'
                })
            
            # 8. Создаем ответ пациента на вопрос (в виде строки)
            response = SurveyResponseDBM(
                scheduled_survey_id=scheduled_survey.id,
                patient_id=patient.id,
                question_id=question.id,
                answer="Хорошо"  # Просто строка, а не словарь
            )
            session.add(response)
            await session.flush()
            
            # Сохраняем данные для вывода
            schedule_id = scheduled_survey.id
            survey_title = survey.title
            patient_name = patient.full_name
            doctor_id = doctor.id
            start_date = scheduled_survey.start_date
            end_date = scheduled_survey.end_date
            next_time = scheduled_survey.next_scheduled_time
            response_data = {
                'id': response.id,
                'question': question.question_text,
                'answer': response.answer,
                'answered_at': response.creation_dt,
            }
            
            await session.commit()
            
            print("\nРезультат:")
            print(f"Создано расписание опросов (id={schedule_id}):")
            print(f"- Опрос: {survey_title}")
            print(f"- Для пациента: {patient_name}")
            print(f"- Назначил доктор: {doctor_id}")
            print(f"- Период: с {start_date} по {end_date}")
            print(f"- Следующий опрос: {next_time}")
            
            print("\nСозданные напоминания:")
            for reminder in reminder_data:
                print(f"  Напоминание #{reminder['number']}:")
                print(f"    ID: {reminder['id']}")
                print(f"    Запланировано на: {reminder['time']}")
                print(f"    Статус: {reminder['status']}")
            
            print("\nСоздан ответ на опрос:")
            print(f"  ID ответа: {response_data['id']}")
            print(f"  Вопрос: {response_data['question']}")
            print(f"  Ответ: {response_data['answer']}")
            print(f"  Время ответа: {response_data['answered_at']}")

        except Exception as e:
            await session.rollback()
            print(f"Ошибка: {str(e)}")
            raise

if __name__ == "__main__":
    asyncio.run(main())