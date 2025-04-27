from shared.sqladmin_.model_view.common import SimpleMV
from shared.sqlalchemy_db_.sqlalchemy_model import SurveyQuestionDBM, SurveyDBM, QuestionDBM

class SurveyQuestionMV(SimpleMV, model=SurveyQuestionDBM):
    name = "Survey Question"
    name_plural = "Survey Questions"
    icon = "fa-solid fa-link"
    
    column_list = [
        SurveyQuestionDBM.id,
        SurveyQuestionDBM.survey,
        SurveyQuestionDBM.question,
        SurveyQuestionDBM.order_index,
    ]
    
    form_columns = [
        SurveyQuestionDBM.survey,
        SurveyQuestionDBM.question,
        SurveyQuestionDBM.order_index,
    ]
    
    column_details_list = [
        SurveyQuestionDBM.id,
        SurveyQuestionDBM.survey,
        SurveyQuestionDBM.question,
        SurveyQuestionDBM.order_index,
        SurveyQuestionDBM.creation_dt,
    ]
    
    column_sortable_list = [
        SurveyQuestionDBM.id,
        SurveyQuestionDBM.creation_dt,
    ]
    
    column_default_sort = [(SurveyQuestionDBM.id, True)]
    
    column_searchable_list = [
        SurveyQuestionDBM.id,
    ]
    
    column_filters = [
        SurveyQuestionDBM.survey,
        SurveyQuestionDBM.question,
    ]
    
    form_ajax_refs = {
        "survey": {
            "fields": [SurveyDBM.id, SurveyDBM.title],
            "page_size": 10
        },
        "question": {
            "fields": [QuestionDBM.id, QuestionDBM.question_text],
            "page_size": 10
        }
    }