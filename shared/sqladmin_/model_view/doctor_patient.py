from shared.sqladmin_.model_view.common import SimpleMV
from shared.sqlalchemy_db_.sqlalchemy_model import DoctorPatientDBM, UserDBM

class DoctorPatientMV(SimpleMV, model=DoctorPatientDBM):
    name = "Doctor-Patient Relation"
    name_plural = "Doctor-Patient Relations"
    icon = "fa-solid fa-user-doctor"
    
    column_list = [
        DoctorPatientDBM.id,
        DoctorPatientDBM.doctor,
        DoctorPatientDBM.patient,
        DoctorPatientDBM.creation_dt,
    ]
    
    form_columns = [
        DoctorPatientDBM.doctor,
        DoctorPatientDBM.patient,
    ]
    
    column_details_list = [
        DoctorPatientDBM.id,
        DoctorPatientDBM.doctor,
        DoctorPatientDBM.patient,
        DoctorPatientDBM.creation_dt,
    ]
    
    column_sortable_list = [
        DoctorPatientDBM.id,
        DoctorPatientDBM.creation_dt,
    ]
    
    column_default_sort = [(DoctorPatientDBM.id, True)]
    
    column_searchable_list = [
        DoctorPatientDBM.id,
    ]
    
    column_filters = [
        DoctorPatientDBM.doctor,
        DoctorPatientDBM.patient,
    ]
    
    form_ajax_refs = {
        "doctor": {
            "fields": [UserDBM.tg_id, UserDBM.full_name],
            "page_size": 10,
            "filters": {"role": UserDBM.Roles.doctor}  # Фильтр только докторов
        },
        "patient": {
            "fields": [UserDBM.tg_id, UserDBM.full_name],
            "page_size": 10,
            "filters": {"role": UserDBM.Roles.patient}  # Фильтр только пациентов
        }
    }
    
    column_labels = {
        "doctor": "Doctor",
        "patient": "Patient",
        "creation_dt": "Creation Date",
        "modification_dt": "Last Modification"
    }
    
    def on_model_change(self, form, model, is_created):
        """Валидация ролей при создании/изменении связи."""
        if model.doctor.role != UserDBM.Roles.doctor:
            raise ValueError("Selected user must have doctor role")
        if model.patient.role != UserDBM.Roles.patient:
            raise ValueError("Selected user must have patient role")
        super().on_model_change(form, model, is_created)