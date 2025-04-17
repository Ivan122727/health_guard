from aiogram import Router

from tg_bot.handlers.common import common_router

main_router = Router(
    name="main_router"
)

main_router.include_routers(
    common_router,
)