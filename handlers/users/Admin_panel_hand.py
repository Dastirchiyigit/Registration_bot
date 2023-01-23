from aiogram import types
from loader import dp
# from keyboards.inline.admin_tugmalari import Admin_tugmalar
#
# from telebot.apihelper import ApiTelegramException

from aiogram.types import CallbackQuery
from data.config import ADMINS
from aiogram.dispatcher import FSMContext
from states.personalData import PersonalData1
from aiogram.types import Message

@dp.message_handler(chat_id=ADMINS,text_contains="soni")
async def select_category(message: Message):

    #####################FILES ichidan olayapti##############
    with open('users_id.txt') as file:
        talabalar = file.readlines()
    talabalar = [talaba.rstrip() for talaba in talabalar]
    ids_set = set(talabalar)
    ###################################
    xabar = len(ids_set)
    await message.answer(f"Foydalanuvchilar soni:\n{xabar}")



@dp.message_handler(chat_id=ADMINS,text_contains="yubor")
async def select_category(message: Message):

    await message.answer(f"Hozircha faqat text yubora olaman.\nXabarri kiriting:")
    await PersonalData1.yuboriladgan_xabar.set()

###########################

@dp.message_handler(state=PersonalData1.yuboriladgan_xabar)
async def answer_email(message: types.Message, state: FSMContext):
    await message.answer("Xabar Hammaga yuborilmoqda")



    ############ FILE ichidan oqiydi va setga olib,IDlarni unique ekanini taminlaydi######
    with open('users_id.txt') as file:
        talabalar = file.readlines()

    talabalar = [talaba.rstrip() for talaba in talabalar] ##qatorlarri bitta qib list qiladi
    ids_set = set(talabalar)#listni set qiladi
    #################  ids_set da hamma foydalanuvchilar ID lari turubdi
    # Adminlaga yuborish
    for x in ids_set:
        try:
            await dp.bot.send_message(x, message.text)
        except Exception as e:
            # print(e) yoki contnue qlish kk.
            continue
    #Yuborish tugadi.



    await message.answer("DONE !!!\n")
    await state.finish()






