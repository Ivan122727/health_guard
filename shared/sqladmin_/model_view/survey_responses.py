from shared.sqladmin_.model_view.common import SimpleMV
from shared.sqlalchemy_db_.sqlalchemy_model import (
    SurveyResponseDBM, 
    UserDBM, 
    QuestionDBM,
    ScheduledSurveyDBM
)

class SurveyResponseMV(SimpleMV, model=SurveyResponseDBM):
    name = "Survey Response"
    name_plural = "Survey Responses"
    icon = "fa-solid fa-reply"
    
    column_list = [
        SurveyResponseDBM.id,
        SurveyResponseDBM.patient,
        SurveyResponseDBM.question,
        SurveyResponseDBM.answer,
        SurveyResponseDBM.scheduled_time,
        SurveyResponseDBM.scheduled_survey,
        SurveyResponseDBM.creation_dt,
    ]
    
    form_columns = [
        SurveyResponseDBM.patient,
        SurveyResponseDBM.question,
        SurveyResponseDBM.answer,
        SurveyResponseDBM.scheduled_time,
        SurveyResponseDBM.scheduled_survey,
    ]
    
    column_details_list = [
        SurveyResponseDBM.id,
        SurveyResponseDBM.patient,
        SurveyResponseDBM.question,
        SurveyResponseDBM.answer,
        SurveyResponseDBM.scheduled_time,
        SurveyResponseDBM.scheduled_survey,
        SurveyResponseDBM.creation_dt,
    ]
    
    column_sortable_list = [
        SurveyResponseDBM.id,
        SurveyResponseDBM.creation_dt,
    ]
    
    column_default_sort = [(SurveyResponseDBM.creation_dt, True)]
    
    column_searchable_list = [
        SurveyResponseDBM.id,
        SurveyResponseDBM.answer,
        SurveyResponseDBM.patient_id,
    ]
    
    column_filters = [
        SurveyResponseDBM.patient,
        SurveyResponseDBM.question,
        SurveyResponseDBM.scheduled_survey,
    ]
    
    form_ajax_refs = {
        "patient": {
            "fields": [UserDBM.tg_id, UserDBM.full_name],
            "page_size": 10,
            "filters": {"role": UserDBM.Roles.patient}
        },
        "question": {
            "fields": [QuestionDBM.id, QuestionDBM.question_text],
            "page_size": 10
        },
        "scheduled_survey": {
            "fields": [ScheduledSurveyDBM.id, ScheduledSurveyDBM.survey_id],
            "page_size": 10
        }
    }
    
    column_labels = {
        "patient": "Patient",
        "question": "Question",
        "answer": "Answer",
        "scheduled_survey": "Scheduled Survey",
        "creation_dt": "Response Date",
        "modification_dt": "Last Modification"
    }
    