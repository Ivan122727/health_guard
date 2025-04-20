from aiogram import Router

from tg_bot.handlers.doctor import create_survey_router, schedule_survey_router

doctor_main_router =  Router()

doctor_main_router.include_routers(
    create_survey_router.router,
    schedule_survey_router.router,
)