from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup


def menu_btn():
    design = [[
        InlineKeyboardButton(text = "It",callback_data="it")
    ]]
    reply_markup = InlineKeyboardMarkup(inline_keyboard = design)
    return reply_markup