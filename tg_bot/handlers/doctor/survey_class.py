from typing import List, Dict, Optional
from dataclasses import dataclass, field
from uuid import uuid4

@dataclass
class Question:
    id: str = field(default_factory=lambda: str(uuid4()))
    text: Optional[str] = None
    options: Optional[List[str]] = None
    is_active: bool = True

class Survey:
    def __init__(self):
        self.questions: Dict[str, Question] = {}  # id: Question
        self.current_question_id: Optional[str] = None
        self.count_active_questions = 0

    def add_question(
            self, 
            text: Optional[str] = None, 
            options: Optional[List[str]] = None
        ) -> str:
        """Добавляет новый вопрос и делает его текущим"""
        question = Question(text=text, options=options)
        self.questions[question.id] = question
        self.current_question_id = question.id
        self.count_active_questions += 1
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
            new_options: Optional[List[str]] = None
        ):
        """Редактирует существующий вопрос"""
        if question_id in self.questions:
            question = self.questions[question_id]
            if new_text:
                question.text = new_text
            if new_options:
                question.options = new_options
    
    def remove_question(self, question_id: str):
        """Удаляет вопрос, сохраняя порядок остальных"""
        if question_id in self.questions:
            # Деактивируем вместо полного удаления для сохранения порядка
            self.questions[question_id].is_active = False
            self.count_active_questions -= 1

            # Если удаляем текущий вопрос, сбрасываем указатель
            if self.current_question_id == question_id:
                self.current_question_id = None
    
    def get_active_questions(self) -> List[Question]:
        """Возвращает список активных вопросов в порядке добавления"""
        return [q for q in self.questions.values() if q.is_active]
    
    def get_question_by_id(self, question_id: str) -> Optional[Question]:
        """Возвращает вопрос по ID"""
        return self.questions.get(question_id)
    
    def set_current_question(self, question_id: str):
        """Устанавливает текущий вопрос"""
        if question_id in self.questions:
            self.current_question_id = question_id