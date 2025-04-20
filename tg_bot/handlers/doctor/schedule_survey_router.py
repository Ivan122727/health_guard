from typing import Optional
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from shared.sqlalchemy_db_.sqlalchemy_model import UserDBM, ScheduledSurveyDBM 
from tg_bot.handlers.common.message_service import MessageService
from tg_bot.keyboards import DoctorAction, DoctorKeyboard
from tg_bot.blanks import DoctorBlank
from tg_bot.states.survey import ScheduleSurveyStates
from tg_bot.handlers.doctor.schedule_survey_service import ScheduleSurveyService

router = Router()

@router.callback_query(F.data.startswith(DoctorAction.CANCEL_SCHEDULING.value))
async def hadle_cancel_scheduling(
    callback_query: CallbackQuery,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM]
):
    await ScheduleSurveyService.clear_schedule_data(
        state=state,
    )

    await MessageService.edith_managed_message(
        bot=callback_query.bot,
        user_id=user_dbm.tg_id,
        text=blank.get_default_blank(user_dbm.full_name),
        reply_markup=keyboard.get_default_keyboard(),
        state=state,
        previous_message_key="start_msg_id",
        message_id_storage_key="start_msg_id",
        message=callback_query.message,
        new_state=None
    )

async def proccess_hadle_shoose_type_survey(
    message: Message,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM],
    from_cq: bool = True
):
    message_from_cq = message if from_cq else None

    await MessageService.edith_managed_message(
        bot=message.bot,
        user_id=user_dbm.tg_id,
        text=blank.get_survey_scheduling_blank(),
        reply_markup=keyboard.get_survey_schedule_type_keyboard(),
        state=state,
        previous_message_key="start_msg_id",
        message_id_storage_key="start_msg_id",
        message=message_from_cq,
        new_state=ScheduleSurveyStates.waiting_choose_type_survey
    )

    if not from_cq:
        await MessageService.remove_previous_message(
            bot=message.bot,
            user_id=user_dbm.tg_id,
            message_id=message.message_id,
        )    

@router.callback_query(F.data.startswith(DoctorAction.SCHEDULE_SURVEY.value))
async def handle_choose_type_survey_cq(
    callback_query: CallbackQuery,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM]
):
    await proccess_hadle_shoose_type_survey(
        message=callback_query.message,
        state=state,
        keyboard=keyboard,
        blank=blank,
        user_dbm=user_dbm,
    )

@router.message(ScheduleSurveyStates.waiting_choose_type_survey)
async def handle_choose_type_survey(
    message: Message,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM]
):
    await proccess_hadle_shoose_type_survey(
        message=message,
        state=state,
        keyboard=keyboard,
        blank=blank,
        user_dbm=user_dbm,
        from_cq=False,
    )


async def proccess_hadle_choose_multiple_times_per_day(
    message: Message,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM],
    from_cq: bool = True
):
    message_from_cq = message if from_cq else None

    await ScheduleSurveyService.save_frequency_type_survey(
        state=state,
        frequency_type=ScheduledSurveyDBM.FrequencyType.MULTIPLE_TIMES_PER_DAY
    )

    await MessageService.edith_managed_message(
        bot=message.bot,
        user_id=user_dbm.tg_id,
        text=blank.get_choose_multiple_times_blank(),
        reply_markup=keyboard.get_multiple_times_per_day_keyboard(),
        state=state,
        previous_message_key="start_msg_id",
        message_id_storage_key="start_msg_id",
        message=message_from_cq,
        new_state=ScheduleSurveyStates.waiting_choose_multiple_times_per_day
    )

    if not from_cq:
        await MessageService.remove_previous_message(
            bot=message.bot,
            user_id=user_dbm.tg_id,
            message_id=message.message_id,
        ) 

@router.callback_query(F.data.startswith(DoctorAction.CHOOSE_MULTIPLE_TIMES_PER_DAY.value))
async def hadle_choose_multiple_times_per_day_cq(
    callback_query: CallbackQuery,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM]
):
    await proccess_hadle_choose_multiple_times_per_day(
        message=callback_query.message,
        state=state,
        keyboard=keyboard,
        blank=blank,
        user_dbm=user_dbm,
    )

@router.message(ScheduleSurveyStates.waiting_choose_multiple_times_per_day)
async def handle_choose_type_survey(
    message: Message,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM]
):
    await proccess_hadle_choose_multiple_times_per_day(
        message=message,
        state=state,
        keyboard=keyboard,
        blank=blank,
        user_dbm=user_dbm,
        from_cq=False,
    )


async def proccess_handle_set_times_per_day(
    message: Message,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM],
    from_cq: bool = True,
    times_per_day: Optional[int] = None,
):
    await ScheduleSurveyService.set_times_per_day(
        state=state,
        times_per_day=times_per_day,
    )


    message_from_cq = message if from_cq else None

    await MessageService.edith_managed_message(
        bot=message.bot,
        user_id=user_dbm.tg_id,
        text=blank.get_set_times_per_day_blank(await ScheduleSurveyService.get_times_per_day(state)),
        reply_markup=keyboard.get_multiple_times_per_day_keyboard(flag=False),
        state=state,
        previous_message_key="start_msg_id",
        message_id_storage_key="start_msg_id",
        message=message_from_cq,
        new_state=ScheduleSurveyStates.waiting_set_times_per_day
    )

    if not from_cq:
        await MessageService.remove_previous_message(
            bot=message.bot,
            user_id=user_dbm.tg_id,
            message_id=message.message_id,
        )

@router.callback_query(F.data.startswith(DoctorAction.SET_TIMES_PER_DAY.value))
async def hadle_choose_times_per_day_cq(
    callback_query: CallbackQuery,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM],
):
    times_per_day = await MessageService.get_value_from_callback_data(
        callback_data=callback_query.data,
        default_value=None,
    ) 

    await proccess_handle_set_times_per_day(
        message=callback_query.message,
        state=state,
        keyboard=keyboard,
        blank=blank,
        user_dbm=user_dbm,
        times_per_day=times_per_day
    )

@router.message(ScheduleSurveyStates.waiting_set_times_per_day)
async def hadle_choose_times_per_day(
    message: Message,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM]
):
    await proccess_handle_set_times_per_day(
        message=message,
        state=state,
        keyboard=keyboard,
        blank=blank,
        user_dbm=user_dbm,
        from_cq=False,
    )


async def proccess_hadle_select_once_per_day(
    message: Message,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM],
    from_cq: bool = True
):
    await ScheduleSurveyService.save_frequency_type_survey(
        state=state,
        frequency_type=ScheduledSurveyDBM.FrequencyType.ONCE_PER_DAY
    )
    
    message_from_cq = message if from_cq else None

    await MessageService.edith_managed_message(
        bot=message.bot,
        user_id=user_dbm.tg_id,
        text=blank.get_once_per_day_blank(),
        reply_markup=keyboard.get_back_to_schedule_type_keyboard(),
        state=state,
        previous_message_key="start_msg_id",
        message_id_storage_key="start_msg_id",
        message=message_from_cq,
        new_state=ScheduleSurveyStates.waiting_choose_once_per_day
    )

    if not from_cq:
        await MessageService.remove_previous_message(
            bot=message.bot,
            user_id=user_dbm.tg_id,
            message_id=message.message_id,
        )    

@router.callback_query(F.data.startswith(DoctorAction.CHOOSE_ONCE_PER_DAY.value))
async def hadle_select_once_per_day_cq(
    callback_query: CallbackQuery,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM]
):
    await proccess_hadle_select_once_per_day(
        message=callback_query.message,
        state=state,
        keyboard=keyboard,
        blank=blank,
        user_dbm=user_dbm,
    )

@router.message(ScheduleSurveyStates.waiting_choose_once_per_day)
async def hadle_select_once_per_day(
    message: Message,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM]
):
    await proccess_hadle_select_once_per_day(
        message=message,
        state=state,
        keyboard=keyboard,
        blank=blank,
        user_dbm=user_dbm,
        from_cq=False,
    )


async def proccess_hadle_select_every_few_days(
    message: Message,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM],
    from_cq: bool = True
):
    await ScheduleSurveyService.save_frequency_type_survey(
        state=state,
        frequency_type=ScheduledSurveyDBM.FrequencyType.EVERY_FEW_DAYS
    )

    message_from_cq = message if from_cq else None

    await MessageService.edith_managed_message(
        bot=message.bot,
        user_id=user_dbm.tg_id,
        text=blank.get_every_few_days_blank(),
        reply_markup=keyboard.get_every_few_days_keyboard(),
        state=state,
        previous_message_key="start_msg_id",
        message_id_storage_key="start_msg_id",
        message=message_from_cq,
        new_state=ScheduleSurveyStates.waiting_choose_every_few_days
    )

    if not from_cq:
        await MessageService.remove_previous_message(
            bot=message.bot,
            user_id=user_dbm.tg_id,
            message_id=message.message_id,
        )    

@router.callback_query(F.data.startswith(DoctorAction.CHOOSE_EVERY_FEW_DAYS.value))
async def hadle_select_every_few_days_cq(
    callback_query: CallbackQuery,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM]
):
    await proccess_hadle_select_every_few_days(
        message=callback_query.message,
        state=state,
        keyboard=keyboard,
        blank=blank,
        user_dbm=user_dbm,
    )

@router.message(ScheduleSurveyStates.waiting_choose_every_few_days)
async def hadle_select_every_few_days(
    message: Message,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM]
):
    await proccess_hadle_select_every_few_days(
        message=message,
        state=state,
        keyboard=keyboard,
        blank=blank,
        user_dbm=user_dbm,
        from_cq=False,
    )


async def proccess_handle_set_interval_days(
    message: Message,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM],
    from_cq: bool = True,
    interval_days: Optional[int] = None,
):
    await ScheduleSurveyService.set_interval_days(
        state=state,
        interval_days=interval_days,
    )

    message_from_cq = message if from_cq else None

    await MessageService.edith_managed_message(
        bot=message.bot,
        user_id=user_dbm.tg_id,
        text=blank.get_every_few_days_time_blank(await ScheduleSurveyService.get_interval_days(state)),
        reply_markup=keyboard.get_multiple_times_per_day_keyboard(flag=False),
        state=state,
        previous_message_key="start_msg_id",
        message_id_storage_key="start_msg_id",
        message=message_from_cq,
        new_state=ScheduleSurveyStates.waiting_set_interval_days
    )

    if not from_cq:
        await MessageService.remove_previous_message(
            bot=message.bot,
            user_id=user_dbm.tg_id,
            message_id=message.message_id,
        )

@router.callback_query(F.data.startswith(DoctorAction.SET_INTERVAL_DAYS.value))
async def handle_set_interval_days_cq(
    callback_query: CallbackQuery,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM],
):
    interval_days = await MessageService.get_value_from_callback_data(
        callback_data=callback_query.data,
        default_value=None,
    ) 

    await proccess_handle_set_interval_days(
        message=callback_query.message,
        state=state,
        keyboard=keyboard,
        blank=blank,
        user_dbm=user_dbm,
        interval_days=interval_days,
    )

@router.message(ScheduleSurveyStates.waiting_set_interval_days)
async def handle_set_interval_days(
    message: Message,
    state: FSMContext,
    keyboard: type[DoctorKeyboard],
    blank: type[DoctorBlank],
    user_dbm: type[UserDBM]
):
    await proccess_handle_set_interval_days(
        message=message,
        state=state,
        keyboard=keyboard,
        blank=blank,
        user_dbm=user_dbm,
        from_cq=False,
    )
