from typing import List, Dict, Optional
from dataclasses import dataclass, field
from uuid import uuid4

@dataclass
class Question:
    text: str
    options: List[str]
    is_active: bool = True
    id: str = field(default_factory=lambda: str(uuid4()))

class Survey:
    def __init__(self):
        self.questions: Dict[str, Question] = {}  # id: Question
        self.current_question_id: Optional[str] = None
    
    def add_question(self, text: str, options: List[str]) -> str:
        """Добавляет новый вопрос и делает его текущим"""
        question = Question(text=text, options=options)
        self.questions[question.id] = question
        self.current_question_id = question.id
        return question.id
    
    def get_current_question(self) -> Optional[Question]:
        """Возвращает текущий вопрос"""
        if self.current_question_id:
            return self.questions.get(self.current_question_id)
        return None
    
    def edit_question(self, question_id: str, new_text: str = None, new_options: List[str] = None):
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
    
    def to_dict(self) -> dict:
        """Сериализует опрос в словарь"""
        return {
            'questions': [
                {
                    'id': q.id,
                    'text': q.text,
                    'options': q.options,
                    'is_active': q.is_active
                } 
                for q in self.questions.values()
            ],
            'current_question_id': self.current_question_id
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Survey':
        """Десериализует опрос из словаря"""
        survey = cls()
        for q_data in data.get('questions', []):
            question = Question(
                id=q_data['id'],
                text=q_data['text'],
                options=q_data['options'],
                is_active=q_data.get('is_active', True)
            )
            survey.questions[question.id] = question
        survey.current_question_id = data.get('current_question_id')
        return survey


# Создание опроса
survey = Survey()

# Добавление вопросов
q1_id = survey.add_question(
    "Как часто вы испытываете головную боль?",
    ["Никогда", "Редко", "Часто"]
)

print(survey.get_active_questions())

q2_id = survey.add_question(
    "Оцените качество сна",
    ["1 - Плохо", "2", "3", "4", "5 - Отлично"]
)

print(survey.get_active_questions())


# Редактирование вопроса
survey.edit_question(
    q1_id,
    new_text="Как часто у вас болит голова?",
    new_options=["Ежедневно", "Несколько раз в неделю", "Редко"]
)

print(survey.get_active_questions())


# Удаление вопроса (деактивация)
survey.remove_question(q2_id)

print(survey.get_active_questions())


# Получение активных вопросов
active_questions = survey.get_active_questions()
for question in active_questions:
    print(f"Вопрос: {question.text}")
    print(f"Варианты: {', '.join(question.options)}")

# Работа с текущим вопросом
survey.set_current_question(q1_id)
current = survey.get_current_question()
if current:
    print(f"Текущий вопрос: {current.text}")