import os
from pathlib import Path
import sys

# Получаем путь к родительской директории
parent_dir = Path(__file__).parent.parent
# Добавляем родительскую директорию в PYTHONPATH
sys.path.append(str(parent_dir))
# Устанавливаем текущую рабочую директорию
os.chdir(parent_dir)

from shared.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from shared.sqlalchemy_db_.sqlalchemy_model import UserDBM, SurveyDBM, DoctorPatientDBM

async def make_test_data():
    get_cached_sqlalchemy_db().reinit()

    async with get_cached_sqlalchemy_db().new_async_session() as async_session:

        doctor_dbm = UserDBM(
            tg_id=380138374,
            role=UserDBM.Roles.doctor,
            full_name="Шакирзянов  Айдар  Анварович"
        )
        async_session.add(doctor_dbm)
        await async_session.flush()

        doctor_dbm = UserDBM(
            tg_id=457643251,
            role=UserDBM.Roles.doctor,
            full_name="Ермолов  Иван  Олегович"
        )
        async_session.add(doctor_dbm)
        await async_session.flush()
        await async_session.refresh(doctor_dbm)

        for i in range(1, 20):
            patient_dbm = UserDBM(
                tg_id=457643251 + i,
                role=UserDBM.Roles.patient,
                full_name=f"Ермолов  Иван  Олегович {i}"
            )
            async_session.add(patient_dbm)
            await async_session.flush()
            await async_session.refresh(patient_dbm)

            doctor_patient = DoctorPatientDBM(
                doctor=doctor_dbm,
                patient=patient_dbm,
            )
            async_session.add(doctor_patient)
            await async_session.flush()
        
        await async_session.commit()

if __name__ == "__main__":
    import asyncio
    asyncio.run(make_test_data())