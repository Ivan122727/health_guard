from typing import Optional, Dict
from dataclasses import dataclass, field
from uuid import uuid4
from datetime import datetime

import sqlalchemy
from sqlalchemy.orm import joinedload

from shared.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from shared.sqlalchemy_db_.sqlalchemy_model import QuestionDBM, SurveyDBM, SurveyReminderDBM, ScheduledSurveyDBM, SurveyQuestionDBM

@dataclass
class PatientSurvey:
    """Класс для управления процессом прохождения опроса пациентом"""
    async def load(self, notification_id: int) -> bool:
        """Загружает опрос по ID уведомления"""
        self.notification_id = notification_id

        async with get_cached_sqlalchemy_db().new_async_session() as async_session:
            try:
                notification_dbm = (await async_session.execute(
                    sqlalchemy.select(SurveyReminderDBM)
                    .where(SurveyReminderDBM.id == notification_id)
                    # .where(SurveyReminderDBM.status == SurveyReminderDBM.ReminderStatus.SENT.value)
                    .options(
                        joinedload(SurveyReminderDBM.scheduled_survey)
                        .joinedload(ScheduledSurveyDBM.survey)
                        .joinedload(SurveyDBM.questions)
                        .joinedload(SurveyQuestionDBM.question)
                    )
                )).scalars().unique().one()

                
                if not notification_dbm.scheduled_survey or not notification_dbm.scheduled_survey.survey:
                    return False

                self.title = notification_dbm.scheduled_survey.survey.title
                self.questions = notification_dbm.scheduled_survey.survey.questions
                self.curr_question_index = 0
                self.count_question = len(self.questions)
                self.answers = {}
                self.scheduled_time = notification_dbm.scheduled_time
                self.scheduled_survey_id = notification_dbm.scheduled_survey_id

                return True
                
            except Exception as e:
                print(f"Error loading survey: {e}")
                return False

    def set_answer(self, text: str):
        self.answers[self.curr_question_index] = text
        self.curr_question_index += 1
        
    def get_current_question(self):
        return self.questions[self.curr_question_index]

    def set_prev_question(self):
        self.curr_question_index = max(0, self.curr_question_index - 1)
