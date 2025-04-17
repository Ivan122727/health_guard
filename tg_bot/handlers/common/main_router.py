from aiogram import Router

from tg_bot.handlers.common import common

common_router =  Router()

common_router.include_routers(
    common.router,
)