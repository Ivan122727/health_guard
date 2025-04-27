from shared.sqladmin_.model_view.common import SimpleMV
from shared.sqlalchemy_db_.sqlalchemy_model import ScheduledSurveyDBM

from sqlalchemy.orm import Session

class ScheduledSurveyMV(SimpleMV, model=ScheduledSurveyDBM):
    name = "ScheduledSurvey"
    name_plural = "ScheduledSurveys"
    icon = "fa-solid fa-calendar-check"
    
    column_list = [
        ScheduledSurveyDBM.id,
        ScheduledSurveyDBM.creation_dt,
        ScheduledSurveyDBM.survey,
        ScheduledSurveyDBM.patient,
        ScheduledSurveyDBM.doctor,
        ScheduledSurveyDBM.frequency_type,
        ScheduledSurveyDBM.times_per_day,
        ScheduledSurveyDBM.interval_days,
        ScheduledSurveyDBM.start_date,
        ScheduledSurveyDBM.end_date,
        ScheduledSurveyDBM.scheduled_times,
        ScheduledSurveyDBM.max_reminders,
        ScheduledSurveyDBM.reminder_interval_hours,
        ScheduledSurveyDBM.is_active,
        ScheduledSurveyDBM.next_scheduled_date,
    ]
    
    form_columns = [
        ScheduledSurveyDBM.survey,
        ScheduledSurveyDBM.doctor_id,
        ScheduledSurveyDBM.patient_id,
        ScheduledSurveyDBM.frequency_type,
        ScheduledSurveyDBM.times_per_day,
        ScheduledSurveyDBM.interval_days,
        ScheduledSurveyDBM.start_date,
        ScheduledSurveyDBM.end_date,
        ScheduledSurveyDBM.scheduled_times,
        ScheduledSurveyDBM.max_reminders,
        ScheduledSurveyDBM.reminder_interval_hours,
        ScheduledSurveyDBM.is_active,
        ScheduledSurveyDBM.next_scheduled_date,
    ]
    
    column_details_list = [
        ScheduledSurveyDBM.survey,
        ScheduledSurveyDBM.patient,
        ScheduledSurveyDBM.doctor,
        ScheduledSurveyDBM.frequency_type,
        ScheduledSurveyDBM.times_per_day,
        ScheduledSurveyDBM.interval_days,
        ScheduledSurveyDBM.start_date,
        ScheduledSurveyDBM.end_date,
        ScheduledSurveyDBM.scheduled_times,
        ScheduledSurveyDBM.max_reminders,
        ScheduledSurveyDBM.reminder_interval_hours,
        ScheduledSurveyDBM.is_active,
        ScheduledSurveyDBM.next_scheduled_date,
    ]
    
    column_sortable_list = [
        ScheduledSurveyDBM.id,
    ]
    
    column_default_sort = [(ScheduledSurveyDBM.id, True)]
    
    column_searchable_list = [
        ScheduledSurveyDBM.patient_id,
        ScheduledSurveyDBM.doctor_id,
        ScheduledSurveyDBM.survey_id,
    ]
    
    column_filters = [
        ScheduledSurveyDBM.frequency_type,
    ]