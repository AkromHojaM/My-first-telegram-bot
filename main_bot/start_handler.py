from aiogram import Dispatcher,types
from aiogram.filters import CommandStart
from buttons.reply_btn import update_btn
from aiogram.filters.command import Command
from aiogram.types.bot_command import BotCommand
from DB.Db import PG
from aiogram.fsm.context import FSMContext
from buttons.inline_btn import menu_btn

from states import state
from states.state import RegisterState
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(msg: types.Message,state: FSMContext):
    obj = PG()
    username = msg.from_user.username
    user_id = msg.from_user.id
    if not obj.select_user(user_id):
        text = (f"*Bizning Botimizga Hush Kelibsiz Bu BOT Ish Boyicha Sizga Yordam Beradi.Agar Bizga Registiratsiya Qilmagan Bolsangiz Regitiratsiya Qilib Oling Qilgan Bolsangiz Menyuga Bosing*\n"
                f"\n"
                f"Ismingizni Kiriting")
        await state.set_state(RegisterState.lastname)
        await msg.answer(text,parse_mode='Markdown')
    else:
        await msg.answer(text="*Siz Registratsiyadan Otib Bolgansiz*",parse_mode='Markdown')

@dp.message(RegisterState.lastname)
async def lastname_handler(msg:types.Message,state: FSMContext):
    obj = PG()
    lastname = msg.text
    await state.update_data(lastname=lastname)
    await state.set_state(RegisterState.firstname)
    await msg.answer(text = "*Familyangizni Kiriting*",parse_mode='Markdown')

@dp.message(RegisterState.firstname)
async def firstname_handler(msg: types.Message,state: FSMContext):
    obj = PG()
    await state.update_data(firstname=msg.text)
    data = await state.get_data()
    lastname = data.get("lastname")
    firstname = data.get('firstname')
    user_id = msg.from_user.id
    obj.add(user_id, lastname,firstname)
    await msg.answer(text = "*Registiratsiya Muvaffaqiyatli Yakunlandi*",parse_mode='Markdown')

update = BotCommand(command="update",description="Update user data")
@dp.message(Command(update))
async def update_handler (msg: types.Message,state: FSMContext):
    await msg.answer(text="*Yangi Ismingizni Kiriting*",parse_mode='Markdown')
    await state.set_state(RegisterState.new_firstname)

@dp.message(RegisterState.new_firstname)
async def new_firstname_handler(msg: types.Message,state: FSMContext):
    name = msg.text
    lastname = msg.text
    await state.update_data(lastname=lastname)
    await msg.answer(text="*Yangi Familyangizni Kiriting*",parse_mode='Markdown')
    await state.set_state(RegisterState.new_lastname)

@dp.message(RegisterState.new_lastname)
async def new_lastname(msg: types.Message,state: FSMContext):
    lastname = msg.text
    await state.update_data(firstname=lastname)
    await state.set_state(RegisterState.submit)
    await msg.answer(text="Tasdiqlash uchun tasdiqlash tugmasini bosing:👇",reply_markup=update_btn())

@dp.message(RegisterState.submit)
async def new_firstname_handler(msg: types.Message,state: FSMContext):
    obj = PG()
    user_id = msg.from_user.id
    data = await state.get_data()
    lastname = data.get("lastname")
    firstname = data.get("firstname")
    obj.update_data(user_id = user_id, lastname=lastname,firstname= firstname)
    await msg.answer(text="*Tasdiqlandi*",parse_mode='Markdown')
    await state.clear()

@dp.message(lambda msg: msg.text == "Foydalanuvchi Haqida Malumot")
async def foydalanuvchi_handler(msg: types.Message,state: FSMContext):
    obj = PG()
    user_id = msg.from_user.id
    data = obj.select_users(user_id=user_id)
    await msg.answer(text=f"Ismi:{data[0][2]}\n"
                          f"Familyasi:{data[0][3]}\n"
                          f"Registratsiya Sanasi:{data[0][4]}\n"
                          f"User Id:{data[0][1]}")

get_info = BotCommand(command="get_info",description="Get info")
@dp.message(Command(get_info))
async def get_info(msg: types.Message):
    await msg.answer(text = "Sizni Qiziqtirgan Kasbni Tanlang?",reply_markup=menu_btn())

last_message_ids = {}

@dp.callback_query(lambda call: call.data == "it")
async def it_handler(call: types.CallbackQuery):
    if call.message.chat.id  in last_message_ids:
        await call.bot.delete_messages(call.message.chat.id, last_message_ids[call.message.from_user.id])
    message = await call.message.answer(text = "It kasbiga Hush Kelibsiz",reply_markup=menu_btn())
    last_message_ids[call.message.chat.id] = message.message_id
    await call.bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id)
