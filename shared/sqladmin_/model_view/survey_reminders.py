from shared.sqladmin_.model_view.common import SimpleMV
from shared.sqlalchemy_db_.sqlalchemy_model import QuestionDBM, SurveyReminderDBM

class SurveyReminderMV(SimpleMV, model=SurveyReminderDBM):
    name = "SurveyReminder"
    name_plural = "SurveyReminders"
    icon = "fa-solid fa-calendar-check"
    
    column_list = [
        SurveyReminderDBM.id,
        SurveyReminderDBM.creation_dt,
        SurveyReminderDBM.scheduled_survey,
        SurveyReminderDBM.reminder_number,
        SurveyReminderDBM.scheduled_time,
        SurveyReminderDBM.status,
        SurveyReminderDBM.completed_at,
    ]
    
    form_columns = [
        SurveyReminderDBM.id,
        SurveyReminderDBM.creation_dt,
        SurveyReminderDBM.scheduled_survey_id,
        SurveyReminderDBM.reminder_number,
        SurveyReminderDBM.scheduled_time,
        SurveyReminderDBM.status,
        SurveyReminderDBM.completed_at,
    ]
    
    column_details_list = [
        SurveyReminderDBM.id,
        SurveyReminderDBM.creation_dt,
        SurveyReminderDBM.scheduled_survey_id,
        SurveyReminderDBM.reminder_number,
        SurveyReminderDBM.scheduled_time,
        SurveyReminderDBM.status,
        SurveyReminderDBM.completed_at,
    ]
    
    column_sortable_list = [
        SurveyReminderDBM.id,
        SurveyReminderDBM.scheduled_survey_id,
    ]
    
    column_default_sort = [(SurveyReminderDBM.id, True)]
    
    column_searchable_list = [
        SurveyReminderDBM.scheduled_survey_id,
    ]
    
    column_filters = [
        SurveyReminderDBM.status,
    ]