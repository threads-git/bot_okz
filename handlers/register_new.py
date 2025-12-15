import asyncio
import datetime
from create_bot import bot
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.utils.chat_action import ChatActionSender
from keyboards.all_kb import get_login_tg, check_data, check_access_kb
from utils.utils import  extract_phone
from utils.database import Database
import os
register_router = Router()
db = Database(os.getenv('DATABASE_NAME'))

class Form(StatesGroup):
    user_name = State()
    user_name_tg = State()
    user_login = State()
    user_phone = State()
    check_state = State()
    check_access = State()

@register_router.message(F.text == 'Зарегистрироваться')
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.clear()
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(2)
        await message.answer('Давайте начнем регистрацию! \nДля начала укажите Фамилию И.О. 😏')
    await state.set_state(Form.user_name)


@register_router.message(F.text, Form.user_name)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.update_data(user_name=message.text, user_id=message.from_user.id, user_name_tg=message.from_user.full_name)
    text = 'Теперь укажите ваш логин, который будет использоваться в боте'

    if message.from_user.username:
        text += ' или нажмите на кнопку ниже и в этом случае вашим логином будет логин из вашего телеграмм: '
        await message.answer(text, reply_markup=get_login_tg())
    else:
        text += ' : '
        await message.answer(text)
    await state.set_state(Form.user_login)

# вариант когда мы берем логин из профиля телеграмм
@register_router.callback_query(F.data, Form.user_login)
async def start_questionnaire_process(call: CallbackQuery, state: FSMContext):
    await call.answer('Беру логин с телеграмм профиля')
    await call.message.edit_reply_markup(reply_markup=None)
    await state.update_data(user_login=call.from_user.username)
    await call.message.answer(f'Теперь укажите номер телефона \n'
                             f'Формат телефона: +7xxxxxxxxxx \n'
                             f'Внимание! Я чувствителен к формату')
    await state.set_state(Form.user_phone)


# вариант когда мы берем логин из введенного пользователем
@register_router.message(F.text, Form.user_login)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.update_data(user_login=message.from_user.username)
    await message.answer(f'Теперь укажите номер телефона \n'
                             f'Формат телефона: +7xxxxxxxxxx \n'
                             f'Внимание! Я чувствителен к формату')
    await state.set_state(Form.user_phone)


@register_router.message(F.text, Form.user_phone)
async def start_questionnaire_process(message: Message, state: FSMContext):
    check_phone = extract_phone(message.text)
    if not check_phone:# or len(check_phone) == 12:# or not (1 <= int(message.text) <= 100):
        await message.reply("Пожалуйста, введите номер по формату +7хххххххххх")
        return
    check_access_db = db.check_access_user(check_phone)
    if not check_access_db:
        await message.reply("⛔️Вам в регистрации отказанно!⛔️\n"
                            "Проверьте номер телефона или\n"
                            "обратитесь сами знаете к кому 😁",
                            reply_markup=check_access_kb())
        await state.set_state(Form.check_access)
        return
    await state.update_data(user_phone=check_phone[0])

    data = await state.get_data()
    caption = f'Пожалуйста, проверьте все ли верно: \n\n' \
              f'<b>Полное имя</b>: {data.get("user_name")}\n' \
              f'<b>Логин в боте</b>: {data.get("user_login")}\n' \
              f'<b>Телефон</b>: {data.get("user_phone")}\n' \

    await message.answer(caption, caption=caption, reply_markup=check_data())
    await state.set_state(Form.check_state)

# сохраняем данные
@register_router.callback_query(F.data == 'correct', Form.check_state)
async def start_questionnaire_process(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    db.add_user(data.get("user_name"), data.get("user_name_tg"), data.get("user_login"),
                data.get("user_phone"),  data.get("user_id"), datetime.date.today())
    await call.answer('Данные сохранены')
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer('Благодарю за регистрацию. Ваши данные успешно сохранены!')
    await state.clear()


# запускаем анкету сначала
@register_router.callback_query(F.data == 'incorrect', Form.check_state)
async def start_questionnaire_process(call: CallbackQuery, state: FSMContext):
    await call.answer('Запускаем сценарий с начала')
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer('Для начала укажите Фамилию И.О. 😏')
    await state.set_state(Form.user_name)

# запускаем выход
@register_router.callback_query(F.data == 'exit_register', Form.check_access)
async def start_questionnaire_process(call: CallbackQuery, state: FSMContext):
    await call.answer('До свидания!')
    await call.message.edit_reply_markup(reply_markup=None)

    await state.clear()
