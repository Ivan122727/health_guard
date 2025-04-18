from aiogram import Router

from tg_bot.handlers.common.main_router import common_router
from tg_bot.handlers.patient.main_router import patient_main_router
from tg_bot.handlers.doctor.main_router import doctor_main_router

main_router = Router(
    name="main_router"
)

main_router.include_routers(
    common_router,
    patient_main_router,
    doctor_main_router
)