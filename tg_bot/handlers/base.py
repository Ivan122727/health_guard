from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет! Я ваш бот-помощник.")

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Список доступных команд:\n/start - Начать работу\n/help - Помощь") 

@router.message()
async def echo_message(message: Message):
    await message.answer(message.text)

@router.callback_query()
async def callback_query(callback_query: CallbackQuery):
    await callback_query.answer()