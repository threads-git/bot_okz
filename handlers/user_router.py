import asyncio
import datetime
import os
import uuid
from aiogram import Router, F, Bot
from aiogram.filters import  Command
from aiogram.fsm.context import FSMContext
from utils.database import Database
from keyboards.all_kb import delay_kb, agreement_kb, main_kb, back_kb, validate_kb
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.utils.chat_action import ChatActionSender
from create_bot import bot

active_requests = {}

user_router = Router()

class Form(StatesGroup):
    delay_time = State()
    back = State()
    telegram_id = State()
    time_delay = State()
    agreement = State() #согласование
    absent = State() # отсутствие
    reason = State() #причина
    validate_medical_state = State()
    validate_vacation_state = State()

@user_router.message(Command('profile'))
@user_router.message(F.text.contains('Профиль'))
async def start_profile(message: Message, state: FSMContext, bot: Bot):
    await bot.send_message(message.from_user.id, 'Считаю Вашу статистику...')
    await asyncio.sleep(1)
    db = Database(os.getenv('DATABASE_NAME'))
    user_delay = db.get_delay(message.from_user.id)
    get_data_max = db.get_data_delay(message.from_user.id)
    profile_message = (
        f"<b>👤 Ваша статистика по опозданиям:</b>\n"
        f"<b>📛 в этом месяце:</b> {user_delay[0]}\n"
        f"<b>📅 Дата последнего опоздания:</b> \n{get_data_max[0]}\n"
    )
    await message.answer(profile_message, caption=profile_message, reply_markup=back_kb())
    await state.set_state(Form.back)

@user_router.message(Command('delay'))
@user_router.message(F.text.contains('Опоздание'))
async def delay(message: Message, state: FSMContext, bot: Bot):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(2)
        await state.update_data(user_id=message.from_user.id)
        await message.answer('Че опять опаздываешь?🤨\nНа сколько???😕', reply_markup=delay_kb())
    await state.set_state(Form.delay_time)

@user_router.callback_query(F.data == 'by15', Form.delay_time)
async def delay(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    db = Database(os.getenv('DATABASE_NAME'))
    db.add_delay(data.get("user_id"), 'by15', datetime.date.today())
    await call.message.answer('Ну ты больше не опаздывай😐', reply_markup=main_kb(data.get("user_id")))
    await call.message.edit_reply_markup(reply_markup=None)
    await state.clear()

@user_router.callback_query(F.data == 'by30', Form.delay_time)
async def delay(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    db = Database(os.getenv('DATABASE_NAME'))
    db.add_delay(data.get("user_id"), 'by30', datetime.date.today())
    await call.message.answer('Ну ты больше не опаздывай😐', reply_markup=main_kb(data.get("user_id")))
    await call.message.edit_reply_markup(reply_markup=None)
    await state.clear()

@user_router.callback_query(F.data == 'by60', Form.delay_time)
async def delay(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    db = Database(os.getenv('DATABASE_NAME'))
    db.add_delay(data.get("user_id"), 'by60', datetime.date.today())
    await call.message.answer('Ну ты больше не опаздывай😐', reply_markup=main_kb(data.get("user_id")))
    await call.message.edit_reply_markup(reply_markup=None)
    await state.clear()

@user_router.callback_query(F.data == 'byhome', Form.delay_time)
async def delay(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer('Сейчас спрошу у начальника...😉 Ожидай...😜')
    await asyncio.sleep(4)
    await call.message.answer('Шутка, давай езжай на работу...🤣🤣🤣')
    await state.clear()

@user_router.callback_query(F.data == 'back', Form.delay_time)
async def delay(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    # db.add_delay(data.get("user_id"), 'by15', datetime.date.today())
    await call.message.answer('Чё? уже не опаздываешь???🤣🤣🤣', reply_markup=main_kb(data.get("user_id")))
    await call.message.edit_reply_markup(reply_markup=None)

@user_router.callback_query(F.data == 'back', Form.back)
# @user_router.message(F.text.contains('Назад'))
async def delay(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await call.message.answer('Ну ты больше не опаздывай😐', reply_markup=main_kb(data.get("user_id")))
    await call.message.edit_reply_markup(reply_markup=None)


@user_router.message(Command('medical'))
@user_router.message(F.text.contains('Больничный'))
async def medical(message: Message, state: FSMContext):
    await state.update_data(user_id=message.from_user.id)
    await message.answer('Уверен?', reply_markup=validate_kb())
    await state.set_state(Form.validate_medical_state)

# @user_router.message(Command('medical'))
# @user_router.message(F.text.contains('Больничный'))
# async def medical(message: Message, state: FSMContext, bot: Bot):
#     async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
#         await state.update_data(user_id=message.from_user.id)
#         data = await state.get_data()
#         fio = db.get_fio(data.get("user_id"))
#         # await message.answer('Уверен?', reply_markup=check_data())
#               db.add_madical(data.get("user_id"), datetime.date.today())
#         #добавить рассылку РН-ам
#         await bot.send_message(375559252, text=f'{fio[0]} ушел на больничный🤧')
#         await message.answer('Выздоравливай!😷\n', reply_markup=main_kb(data.get("user_id")))
#         await state.clear()

@user_router.callback_query(F.data == 'yes', Form.validate_medical_state)
async def medical(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    db = Database(os.getenv('DATABASE_NAME'))
    fio = db.get_fio(data.get("user_id"))
    db.add_madical(data.get("user_id"), datetime.date.today())
    # await call.answer('Данные сохранены')
    await call.message.edit_reply_markup(reply_markup=None)
    #добавить рассылку РН-ам
    await bot.send_message(data.get("user_id"), text='Выздоравливай!😷\n', reply_markup=main_kb(data.get("user_id")))
    await bot.send_message(375559252, text=f'{fio[0]} ушел на больничный🤧')
    await state.clear()


# запускаем анкету сначала
@user_router.callback_query(F.data == 'no', Form.validate_medical_state)
async def medical(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await bot.send_message(data.get("user_id"), 'Уже поправился?😏 Так быстро?🤣')
    await call.message.edit_reply_markup(reply_markup=None)
    await state.clear()


@user_router.message(Command('vacation'))
@user_router.message(F.text.contains('Отпуск'))
async def vacation(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(user_id=message.from_user.id)
    await message.answer('Уверен?', reply_markup=validate_kb())
    await state.set_state(Form.validate_vacation_state)


@user_router.callback_query(F.data == 'yes', Form.validate_vacation_state)
async def vacation(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    db = Database(os.getenv('DATABASE_NAME'))
    fio = db.get_fio(data.get("user_id"))
    db.add_vacation(data.get("user_id"), datetime.date.today())
    await call.answer('Отличного отдыха!\n', reply_markup=main_kb(data.get("user_id")))
    await call.message.edit_reply_markup(reply_markup=None)
    # добавить рассылку РН-ам

    await bot.send_message(375559252, text=f'{fio[0]} ушел в отпуск\nНе забудь отметить в отсутствующих✍️ и\n'
                                           f'сообщить координаторам, если ранее не сообщили!🗣')
    await state.clear()

@user_router.callback_query(F.data == 'no', Form.validate_vacation_state)
async def vacation(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await bot.send_message(data.get("user_id"), 'Отпуск отменяется?! 🤣')
    await call.message.edit_reply_markup(reply_markup=None)
    await state.clear()


# @user_router.message(Command('vacation'))
# @user_router.message(F.text.contains('Отпуск'))
# async def vacation(message: Message, state: FSMContext, bot: Bot):
#     async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
#         await state.update_data(user_id=message.from_user.id)
#         data = await state.get_data()
#         fio = db.get_fio(data.get("user_id"))
#         db.add_vacation(data.get("user_id"), datetime.date.today())
#         #добавить рассылку РН-ам
#         await bot.send_message(375559252, text=f'{fio[0]} ушел в отпуск\nНе забудь отметить в отсутствующих✍️ и\n'
#                                                f'сообщить координаторам, если ранее не сообщили!🗣')
#         await message.answer('Отличного отдыха!\n', reply_markup=main_kb(data.get("user_id")))
#         await state.clear()


@user_router.message(Command('absent'))
@user_router.message(F.text.contains('Отсутствие'))
async def absent(message: Message, state: FSMContext, bot: Bot):
    # async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
    await state.update_data(user_id=message.from_user.id, chat_id=message.chat.id)
    await message.answer('Укажи причину и период отсутствия (одним сообщением) 🤨')
    await state.set_state(Form.reason)


@user_router.message(F.text, Form.reason)
async def absent(message: Message, state: FSMContext):
    await state.update_data(reason=message.text, user_id=message.from_user.id, chat_id=message.chat.id)
    data = await state.get_data()
    db = Database(os.getenv('DATABASE_NAME'))
    fio = db.get_fio(data.get("user_id"))
    request_id = str(uuid.uuid4())
    # question = message.text
    # Сохраняем запрос
    active_requests[request_id] = {
        "from_user_id": message.from_user.id,
        "note": data.get("reason")
        # "from_username": message.from_user.username,
        # "question": question,
        # "target_user_id": 849274173
    }

    await bot.send_message(chat_id=message.from_user.id, text='Направлено на согласование🙃')
    await bot.send_message(849274173, text=f'{fio[0]} запрашивает согласование отсутствия:\n'
                                          f'<b>{data.get("reason")}</b>', reply_markup=agreement_kb(request_id))
    await state.clear()


@user_router.callback_query(F.data.startswith('approve_'))
async def yes_absent(call: CallbackQuery, state: FSMContext):
    request_id = call.data.replace("approve_", "")
    if request_id not in active_requests:
        await call.answer("Запрос устарел")
        return
    request_data = active_requests[request_id]
    await bot.send_message(request_data['from_user_id'], text='Согласовано')
    await call.message.edit_reply_markup(reply_markup=None)
    db = Database(os.getenv('DATABASE_NAME'))
    db.add_absent(request_data['from_user_id'], datetime.date.today(), request_data['note'])
    await call.message.answer("Вы согласовали, Ответ отправлен!")
    await state.clear()
    del active_requests[request_id]

@user_router.callback_query(F.data.startswith('no_approve_'))
async def no_absent(call: CallbackQuery, state: FSMContext):
    request_id = call.data.replace("no_approve_", "")
    if request_id not in active_requests:
        await call.answer("Запрос устарел")
        return
    request_data = active_requests[request_id]
    await bot.send_message(request_data['from_user_id'], text='Не согласовано')
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("Вы не согласовали, Ответ отправлен!")
    await state.clear()
    del active_requests[request_id]









