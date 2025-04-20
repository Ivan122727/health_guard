from typing import List, Dict, Optional
from dataclasses import dataclass, field
from uuid import uuid4

@dataclass
class Question:
    id: str = field(default_factory=lambda: str(uuid4()))
    text: Optional[str] = None
    options: Optional[List[str]] = None
    is_active: bool = True
    is_from_template: bool = False
    template_question_id: Optional[int] = None

class Survey:
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
            return q.template_question_id is not None
        else:
            return q.text is not None and q.options is not None

    def get_active_questions(self) -> List[Question]:
        """Возвращает список активных вопросов в порядке добавления"""
        return [q for q in self.questions.values() if Survey.is_valid_question(q)]
    
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
