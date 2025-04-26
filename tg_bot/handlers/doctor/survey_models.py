from datetime import date, datetime, time
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from uuid import uuid4

from shared.sqlalchemy_db_.sqlalchemy_model import ScheduledSurveyDBM, SurveyDBM, UserDBM

@dataclass
class Question:
    id: str = field(default_factory=lambda: str(uuid4()))
    text: Optional[str] = None
    options: Optional[List[str]] = None
    is_active: bool = True
    is_from_template: bool = False
    template_question_id: Optional[int] = None

class CreatedSurvey:
    _STATE_KEY_SURVEY_DATA = "create_survey"
    _STATE_KEY_EDIT_QUESTION_ID = "create_survey_edit_question_id"
    _STATE_KEY_SURVEY_NOT_CONFIRMED_TITLE = "create_survey_not_confirmed_title"

    def __init__(self):
        self.questions: Dict[str, Question] = {}  # id: Question
        self.current_question_id: Optional[str] = None
        self.title = None

    def edith_survey_title(
            self,
            title: str
    ):
        self.title = title

    def add_question(
            self, 
            text: Optional[str] = None, 
            options: Optional[List[str]] = None,
            is_from_template: bool = False,
            template_question_id: Optional[int] = None
        ) -> str:
        """Добавляет новый вопрос и делает его текущим"""
        question = Question(
            text=text, 
            options=options,
            is_from_template=is_from_template,
            template_question_id=template_question_id,
        )
        self.questions[question.id] = question
        self.current_question_id = question.id
        return question.id
    
    def get_current_question(self) -> Optional[Question]:
        """Возвращает текущий вопрос"""
        if self.current_question_id:
            return self.questions.get(self.current_question_id)
        return None
    
    def edit_question(
            self, 
            question_id: str, 
            new_text: Optional[str] = None, 
            new_options: Optional[List[str]] = None,
            is_from_template: Optional[bool] = None,
            template_question_id: Optional[int] = None,
        ):
        """Редактирует существующий вопрос"""
        if question_id in self.questions:
            question = self.questions[question_id]
            if new_text:
                question.text = new_text
            if new_options:
                question.options = new_options
            if is_from_template and template_question_id:
                question.is_from_template = is_from_template
                question.template_question_id = template_question_id

    
    def remove_question(self, question_id: str):
        """Удаляет вопрос, сохраняя порядок остальных"""
        if question_id in self.questions:
            # Деактивируем вместо полного удаления для сохранения порядка
            self.questions[question_id].is_active = False

            # Если удаляем текущий вопрос, сбрасываем указатель
            if self.current_question_id == question_id:
                try:
                    self.current_question_id = self.get_active_questions()[-1].id
                except IndexError:
                    self.current_question_id = None
    
    @staticmethod
    def is_valid_question(q: Question) -> bool:
        """Проверяет, соответствует ли вопрос критериям валидности"""
        if not q.is_active:
            return False
        if q.is_from_template:
            return not(q.template_question_id is None)
        else:
            return isinstance(q.text, str) and (isinstance(q.options, list) and 1 < len(q.options) < 11)

    def get_active_questions(self) -> List[Question]:
        """Возвращает список активных вопросов в порядке добавления"""
        return [q for q in self.questions.values() if CreatedSurvey.is_valid_question(q)]
    
    def get_question_by_id(self, question_id: str) -> Optional[Question]:
        """Возвращает вопрос по ID"""
        return self.questions.get(question_id)
    
    def set_current_question(self, question_id: str):
        """Устанавливает текущий вопрос"""
        if question_id in self.questions:
            self.current_question_id = question_id
           

    @property
    def count_valid_questions(self) -> int:
        return len(self.get_active_questions())


@dataclass
class Survey:
    survey_dbm: Optional[SurveyDBM] = None
    patient_dbm: Optional[UserDBM] = None
    doctor_dbm: Optional[UserDBM] = None
    frequency_type: Optional[str] = None 
    times_per_day: Optional[int] = None
    interval_days: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    schedule_times: Optional[list[time]] = None
    max_reminders: int = 3
    reminder_interval_hours: int = 2

class ScheduledSurvey:
    _STATE_KEY_SURVEY_DATA = "schedule_survey"
    _STATE_KEY_SELECT_SURVEY_CURRENT_PAGE = "select_survey_current_page"
    _STATE_KEY_SELECT_PATIENT_CURRENT_PAGE = "select_patient_current_page"
    _STATE_KEYS = [
        _STATE_KEY_SURVEY_DATA,
        _STATE_KEY_SELECT_SURVEY_CURRENT_PAGE,
        _STATE_KEY_SELECT_PATIENT_CURRENT_PAGE,
    ]

    def __init__(self):
        self.survey = Survey()

    def set_frequency_type(self, frequency_type: str) -> None:
        if frequency_type in ScheduledSurveyDBM.FrequencyType:
            self.survey.frequency_type = frequency_type
        
    def set_times_per_day(self, times_per_day: int) -> None:
        if self.survey.frequency_type is ScheduledSurveyDBM.FrequencyType.MULTIPLE_TIMES_PER_DAY:
            self.survey.times_per_day = times_per_day
        
    def set_interval_days(self, interval_days: int) -> None:
        if self.survey.frequency_type in ScheduledSurveyDBM.FrequencyType.EVERY_FEW_DAYS:
            self.survey.interval_days = interval_days

    def save_times(self, schedule_times: list[time]) -> None:
        self.survey.schedule_times = schedule_times

    def save_survey_period(self, start_date: date, end_date: date) -> None:
        self.survey.start_date = start_date
        self.survey.end_date = end_date

    def save_selected_survey(self, survey_dbm: SurveyDBM):
        self.survey.survey_dbm = survey_dbm

    def get_selected_survey(self):
        return self.survey.survey_dbm
    
    def save_selected_patient(self, user_dbm: UserDBM):
        self.survey.patient_dbm = user_dbm

    def get_selected_patient(self):
        return self.survey.patient_dbm

    def get_survey(self):
        return self.survey