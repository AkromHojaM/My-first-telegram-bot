from aiogram.types import ReplyKeyboardMarkup,KeyboardButton


def update_btn():
    design = [
        [KeyboardButton(text="Malumotlarni Tog'riligini tasdiqlash")]
        ,[KeyboardButton(text="Foydalanuvchi Haqida Malumot")],
        [KeyboardButton(text ="Ishla Haqida Malumot")]
            ]
    markup = ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True, one_time_keyboard=True)
    return markup
