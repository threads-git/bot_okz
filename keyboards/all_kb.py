from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from create_bot import admins

def main_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="Опоздание"), KeyboardButton(text="Больничный")],
        [KeyboardButton(text="Отпуск"), KeyboardButton(text="Отсутствие")],
        # [KeyboardButton(text="DayOFF"),
         [KeyboardButton(text="👤 Профиль")]
    ]

    if user_telegram_id in admins:
        kb_list.append([KeyboardButton(text="⚙️ Админ панель")])
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard


def back_kb():
    kb_list = [
        [InlineKeyboardButton(text="Назад", callback_data='back')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def reconsider_kb():
    kb_list = [
        [InlineKeyboardButton(text="Передумал", callback_data='back1')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def delay_kb():
    kb_list = [
        [InlineKeyboardButton(text="до 15 минут", callback_data='by15')],
        [InlineKeyboardButton(text="до 30 минут", callback_data='by30')],
        [InlineKeyboardButton(text="до часу", callback_data='by60')],
        [InlineKeyboardButton(text="уже нет смысла, возвращаюсь домой", callback_data='byhome')],
        [InlineKeyboardButton(text="Назад", callback_data='back')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def register_kb():
    kb_list = [
        [KeyboardButton(text="Зарегистрироваться")]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard

def check_data():
    kb_list = [
        [InlineKeyboardButton(text="✅Все верно", callback_data='correct')],
        [InlineKeyboardButton(text="❌Заполнить сначала", callback_data='incorrect')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def validate_kb():
    kb_list = [
        [InlineKeyboardButton(text="✅Все верно", callback_data='yes')],
        [InlineKeyboardButton(text="❌Отменить", callback_data='no')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def get_login_tg():
    kb_list = [
        [InlineKeyboardButton(text="Использовать мой логин с ТГ", callback_data='in_login')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def check_access_kb():
    kb_list = [
        [InlineKeyboardButton(text="🔚Выйти", callback_data='exit_register')],
        [InlineKeyboardButton(text="❌Заполнить сначала", callback_data='incorrect')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def agreement_kb(request_id):
    kb_list = [
        [InlineKeyboardButton(text="✅Согласовать", callback_data=f'approve_{request_id}')],
        [InlineKeyboardButton(text="❌Отклонить", callback_data=f'no_approve_{request_id}')]
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def adm_kb():
    kb_list = [
        [KeyboardButton(text="Общая статистика"), KeyboardButton(text="Добавить User")],
        [KeyboardButton(text="Удалить User")], [KeyboardButton(text="На главную")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard