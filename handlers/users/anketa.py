from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
# from data.config import My_users
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp
from states.personalData import PersonalData1

import logging

from aiogram import Dispatcher

from data.config import ADMINS
from keyboards.inline.Inline import keyboeards


@dp.message_handler(CommandStart())
async def enter_test(message: types.Message):
###########################################################
    faylnomi = 'users_id.txt'
    with open(faylnomi, 'a+') as fayl:
        fayl.write(f'{message.from_user.id}\n')
    ##########FILE ichiga harr gal start bosganda ID larri yozadi#####

    await message.answer(f"*👋Salom, {message.from_user.full_name}\!*\n🤖Bot orqali mahsulotlarimizga buyurma berishinggiz mumkin", parse_mode=types.ParseMode.MARKDOWN_V2 , reply_markup=keyboeards)
    await message.answer("*Ismingizni kiriting: *" , parse_mode=types.ParseMode.MARKDOWN_V2  )
    await PersonalData1.fullName.set()

    ######################
    malumot = f"{message.from_user.full_name}\nId->{message.from_user.id}\nUsername-> @{message.from_user.username}"
    malumot = f"<a href='tg://user?id={message.from_user.id}'>👉{message.from_user.full_name.upper()}👈</a>.\n@{message.from_user.username}"
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, f"Yangi foydalanuvchi\n {malumot}!\nhozicha ZAKAZ buyurmadi!")

        except Exception as err:
            logging.exception(err)


@dp.message_handler(state=PersonalData1.fullName)
async def answer_fullname(message: types.Message, state: FSMContext):
    fullname = message.text

    await state.update_data(
        {"name": fullname}
    )

    await message.answer("Yashash manzilingiz:", parse_mode=types.ParseMode.MARKDOWN_V2 )

    # await PersonalData.email.set()
    await PersonalData1.next()

@dp.message_handler(state=PersonalData1.manzil)
async def answer_email(message: types.Message, state: FSMContext):
    manzil = message.text

    await state.update_data(
        {"email": manzil}
    )
    await message.answer("📲Telefon raqam kiriting:")

    await PersonalData1.next()


@dp.message_handler(state=PersonalData1.phoneNum )
async def answer_phone(message: types.Message, state: FSMContext):
    phone = message.text

    await state.update_data(
        {"phone": phone}
    )
    # Ma`lumotlarni qayta o'qiymiz
    data = await state.get_data()
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")

    msg = "Quyidai ma`lumotlar qabul qilindi‼️:\n\n"
    msg += f"Username - @{message.from_user.username}\n"
    msg += f"Nikname - {message.from_user.full_name}\n"
    msg += f"Botga bergan malumoti\n\nIsmi - {name}\n"
    msg += f"Manzil - {email}\n"
    msg += f"Telefon:  {phone}"
    await message.answer("✨Buyurtma qabul qilindi!,Agar malumotlarni to'g'ri kiritgan bo'lsanggiz,"
                         "🛂Adminlar sizga yaqin Daqiqalar⏱ichida bog'lanishadilar\n"
                         "📝Malumotlariz xato bo'lsa  /START  tugmasini bosin va qayta to'ldiring")

    # State dan chiqaramiz
    # 1-variant
    # await state.finish()

    # 2-variant
    # await state.reset_state()

    # 3-variant. Ma`lumotlarni saqlab qolgan holda
    await state.reset_state(with_data=False)
    #####################333
    #Adminlaga yuborish
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, msg)

        except Exception as err:
            logging.exception(err)


########################################################


