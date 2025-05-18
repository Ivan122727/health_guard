from aiogram import Router

from tg_bot.handlers.patient import patient_connect_to_doctor_router
from tg_bot.handlers.patient import testing_patient

patient_main_router =  Router()

patient_main_router.include_routers(
    patient_connect_to_doctor_router.router,
    testing_patient.router,
)