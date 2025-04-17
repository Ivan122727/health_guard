from aiogram import Router

from tg_bot.handlers.common import user_router

common_router =  Router()

common_router.include_routers(
    user_router.router,
)