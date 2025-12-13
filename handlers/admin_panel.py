from aiogram import F, Router
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender
from create_bot import admins, bot
from utils.database import Database
from keyboards.all_kb import adm_kb, back_kb, main_kb, validate_kb
from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from utils.utils import extract_phone
import os

admin_router = Router()
db = Database(os.getenv('DATABASE_NAME'))
class Form(StatesGroup):
    user_id = State()
    user_name_adm = State()
    user_phone_adm = State()
    del_user = State()
    validation_del_user = State()


@admin_router.message((F.text.endswith('Админ панель')) & (F.from_user.id.in_(admins)))
async def admin_panel(message: Message, state: FSMContext):
    await state.update_data(user_id=message.from_user.id)
    await message.answer('Меню Администоратора', reply_markup=adm_kb())


@admin_router.message((F.text.endswith('Общая статистика')) & (F.from_user.id.in_(admins)))
async def get_profile(message: Message):
    async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):
        count_users = db.get_all_users()
        all_user_info = list(db.get_all_user_info())
        admin_text = (
            f'👥 Количество зарегистрированных: <b>{count_users[0]}</b>. Вот, короткая информация по каждому:\n\n')
        for el in all_user_info:
            admin_text += (
            f'👤 ФИО: {el[0]}\n'
            f'📝 Опозданий на 15 мин: {el[1]}\n'
            f'📝 Опозданий на 30 мин: {el[2]}\n'
            f'📝 Опозданий на 60 мин: {el[3]}\n'
            f'📝 Отпуск: {el[4]}\n'
            f'📝 Больничный: {el[5]}\n\n'
            )
    await message.answer(admin_text, reply_markup=back_kb())


@admin_router.callback_query(F.data == 'back')
async def admin_panel(call: CallbackQuery):
    await call.message.answer('Возврат в прошлое меню', reply_markup=adm_kb())
    await call.message.edit_reply_markup(reply_markup=None)

@admin_router.callback_query(F.data == 'На главную"')
@admin_router.message(F.text.contains('На главную'))
async def admin_panel(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await call.answer('Возвращаю на главную', reply_markup=main_kb(data.get("user_id")))

@admin_router.message(F.text == 'Добавить User')
async def add_user(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Для начала укажите в таком формате: Фамилию И.О.😏')
    await state.set_state(Form.user_name_adm)

@admin_router.message(F.text, Form.user_name_adm)
async def add_user(message: Message, state: FSMContext):
    await state.update_data(user_name_adm=message.text)
    await message.answer(f'Теперь укажите номер телефона \n'
                             f'Формат телефона: +7xxxxxxxxxx \n'
                             f'Внимание! Я чувствителен к формату')
    await state.set_state(Form.user_phone_adm)

@admin_router.message(F.text, Form.user_phone_adm)
async def add_user(message: Message, state: FSMContext):
    check_phone = extract_phone(message.text)
    if not check_phone:  # or len(check_phone) == 12:# or not (1 <= int(message.text) <= 100):
        await message.reply("Пожалуйста, введите номер по формату +7хххххххххх")
        return
    await state.update_data(user_phone_adm=check_phone[0])
    data = await state.get_data()
    db.adm_add_user(data.get("user_name_adm"), data.get("user_phone_adm"))
    await message.answer('Данные сохранены', reply_markup=adm_kb())
    await state.clear()

@admin_router.message(F.text == 'Удалить User')
async def del_user(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f'Укажите Фамилию, кого следует удалить\n'
                             f'⛔️Будет удалена вся информация!⛔\n️'
        )
    await state.set_state(Form.del_user)

@admin_router.message(F.text, Form.del_user)
async def del_user(message: Message, state: FSMContext):
    await state.update_data(user_name_adm=message.text, user_id=message.from_user.id)
    await message.answer('Уверен?', reply_markup=validate_kb())
    await state.set_state(Form.validation_del_user)

@admin_router.callback_query(F.data == 'yes', Form.validation_del_user)
async def del_user(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_name = data.get("user_name_adm")
    tgid = db.get_tg_id(user_name)
    db.adm_del_user(user_name, tgid)
    await call.message.edit_reply_markup(reply_markup=None)
    await bot.send_message(data.get("user_id"), f'{user_name} удален!', reply_markup=adm_kb())
    await state.clear()

@admin_router.callback_query(F.data == 'no', Form.validation_del_user)
async def del_user(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await bot.send_message(data.get("user_id"), 'Удаление отменено!', reply_markup=adm_kb())
    await call.message.edit_reply_markup(reply_markup=None)
    await state.clear()