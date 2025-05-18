from datetime import datetime
import os
from pathlib import Path
import sys

import pytz

# Получаем путь к родительской директории
parent_dir = Path(__file__).parent.parent
# Добавляем родительскую директорию в PYTHONPATH
sys.path.append(str(parent_dir))
# Устанавливаем текущую рабочую директорию
os.chdir(parent_dir)

from shared.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from shared.sqlalchemy_db_.sqlalchemy_model import UserDBM, SurveyDBM, DoctorPatientDBM, SurveyQuestionDBM, QuestionDBM

async def make_test_data():
    get_cached_sqlalchemy_db().reinit()

    async with get_cached_sqlalchemy_db().new_async_session() as async_session:
        for i in range(1, 20):
            doctor_dbm = UserDBM(
                tg_id=380138374 + i,
                role=UserDBM.Roles.doctor,
                full_name=f"Доктор Докторович {i}"
            )
            async_session.add(doctor_dbm)
            await async_session.flush()

        await async_session.commit()

if __name__ == "__main__":
    import asyncio
    asyncio.run(make_test_data())