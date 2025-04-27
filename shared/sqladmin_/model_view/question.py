from shared.sqladmin_.model_view.common import SimpleMV
from shared.sqlalchemy_db_.sqlalchemy_model import QuestionDBM, UserDBM

from sqlalchemy.orm import Session

class QuestionMV(SimpleMV, model=QuestionDBM):
    name = "Question"
    name_plural = "Questions"
    icon = "fa-solid fa-clipboard-question"
    
    column_list = [
        QuestionDBM.id,
        QuestionDBM.author,  # Для отображения в списке
        QuestionDBM.question_text,
        QuestionDBM.question_type,
        QuestionDBM.answer_options,
        QuestionDBM.is_public,
    ]
    
    form_columns = [
        QuestionDBM.question_text,
        QuestionDBM.question_type,
        QuestionDBM.answer_options,
        QuestionDBM.is_public,
    ]
    
    column_details_list = [
        QuestionDBM.id,
        QuestionDBM.author,
        QuestionDBM.question_text,
        QuestionDBM.question_type,
        QuestionDBM.answer_options,
        QuestionDBM.is_public,
    ]
    
    column_sortable_list = [
        QuestionDBM.id,
    ]
    
    column_default_sort = [(QuestionDBM.id, True)]
    
    column_searchable_list = [
        QuestionDBM.question_text,
        QuestionDBM.id,
    ]
    
    column_filters = [
        QuestionDBM.is_public,
        QuestionDBM.question_type,
        QuestionDBM.question_type,
    ]