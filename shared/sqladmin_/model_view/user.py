import sqlalchemy
from wtforms import SelectField

from shared.sqladmin_.model_view.common import SimpleMV
from shared.sqlalchemy_db_.sqlalchemy_model import UserDBM


class UserMV(SimpleMV, model=UserDBM):
    name = "User"
    name_plural = "Users"
    column_list = [
        UserDBM.id,
        UserDBM.creation_dt,
        UserDBM.tg_id,
        UserDBM.email,
        UserDBM.phone,
        UserDBM.full_name,
        UserDBM.role,
        UserDBM.is_active,
    ]
    form_columns = [
        UserDBM.tg_id,
        UserDBM.email,
        UserDBM.phone,
        UserDBM.full_name,
        UserDBM.role,
        UserDBM.is_active,
    ]
    form_overrides = {
        UserDBM.role.key: SelectField
    }
    form_args = {
        UserDBM.role.key: {
            "choices": [(role, role) for role in UserDBM.Roles.to_set()],
            "description": "Выберите роль пользователя"
        }
    }
    column_sortable_list = sqlalchemy.inspect(UserDBM).columns
    column_default_sort = [
        (UserDBM.creation_dt, True)
    ]

    column_searchable_list = [
        UserDBM.tg_id,
        UserDBM.full_name,
        UserDBM.role,
    ]
