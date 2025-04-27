from shared.sqladmin_.model_view.common import SimpleMV
from shared.sqlalchemy_db_.sqlalchemy_model import SurveyDBM, UserDBM
import sqlalchemy

class SurveyMV(SimpleMV, model=SurveyDBM):
    name = "Survey"
    name_plural = "Surveys"
    icon = "fa-solid fa-clipboard-question"
    
    column_list = [
        SurveyDBM.id,
        SurveyDBM.title,
        SurveyDBM.description,
        'author',  # Показываем через relationship
        SurveyDBM.is_active,
    ]
    
    form_columns = [
        SurveyDBM.title,
        SurveyDBM.description,
        'author',  # Используем relationship
        SurveyDBM.is_active
    ]
    
    form_ajax_refs = {
        'author': {
            'fields': (UserDBM.tg_id, UserDBM.full_name),
            'page_size': 10
        }
    }
    
    # Остальные атрибуты остаются без изменений
    column_details_list = [
        SurveyDBM.id,
        SurveyDBM.title,
        SurveyDBM.description,
        'author',
        SurveyDBM.is_active,
        "questions"
    ]
    
    column_sortable_list = [
        SurveyDBM.id,
        SurveyDBM.title,
        SurveyDBM.is_active
    ]
    
    column_default_sort = [(SurveyDBM.creation_dt, True)]
    
    column_searchable_list = [
        SurveyDBM.title,
        SurveyDBM.description,
        "author.full_name"
    ]
    
    column_filters = [
        SurveyDBM.is_active,
        "author"
    ]