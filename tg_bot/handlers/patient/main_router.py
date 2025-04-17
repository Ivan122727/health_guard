from aiogram import Router

from tg_bot.handlers.patient import patient_router

patient_main_router =  Router()

patient_main_router.include_routers(
    patient_router.router,
)