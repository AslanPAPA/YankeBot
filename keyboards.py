from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton

#/START
start = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='👤 Профиль', callback_data='profile')],
    [InlineKeyboardButton(text='🛒 Магазин', callback_data='shop')],
    [InlineKeyboardButton(text='⚙️ Парсер', callback_data='parser')],
    [InlineKeyboardButton(text='📋 Инструкция', callback_data='instruction')],
    [InlineKeyboardButton(text='👋 Мы', callback_data='aboutUs')]
])


#КНОПКА ПРОФИЛЬ
profile = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🪪 Аккаунты', callback_data='accounts'),
     InlineKeyboardButton(text='💎 VIP', callback_data='inDev')],
    [InlineKeyboardButton(text='📋 Задания', callback_data='task'),
     InlineKeyboardButton(text='🛒 Магазин', callback_data='inDev')],
    [InlineKeyboardButton(text='⬅️ НАЗАД', callback_data='backToStart')]
])


#КНОПКА АККАУНТЫ
accounts = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='➕ Добавить аккаунт', callback_data='addAcc')],
    [InlineKeyboardButton(text='🗑️ Удалить аккаунт', callback_data='delAcc')],
    [InlineKeyboardButton(text='️⬅️ НАЗАД', callback_data='backToPrfl')]
])


#КНОПКА ДОБАВЛЕНИЕ АККАУНТА
addAccount = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⬅️ НАЗАД', callback_data='backToAcc')]
])


#КНОПКА VIP
vip = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='️⬅️ НАЗАД', callback_data='backToPrfl')]
])


#КНОПКИ ВЫБОР ЗАДАНИЯ
chooseTask = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='💬 Рассылка', callback_data='rassilka')],
    [InlineKeyboardButton(text='⬅️ НАЗАД', callback_data='backToPrfl')]
])


#КНОПКА РАССЫЛКА
chooseRassilka = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📩 Рассылка в ЛС', callback_data='RassInLs')],
    [InlineKeyboardButton(text='✉️ Рассылка по чатам', callback_data='RassInChats')],
    [InlineKeyboardButton(text='⬅️ НАЗАД', callback_data='backToTask')]
])

#КНОПКИ РАССЫЛКА В ЛС
rassilkaInLs = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⬅️ НАЗАД', callback_data='backToRass')]
])


#КНОПКИ РАССЫЛКА В ЧАТЫ
rassilkaInChats = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⬅️ НАЗАД', callback_data='backToRass')]
])


#КНОПКА МАГАЗИН
shop = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='️⬅️ НАЗАД', callback_data='backToStart')]
])


#КНОПКА ВЫБОР ПАРСИНГА
chooseParsing = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='1️⃣ Парсинг сообщества ВК', callback_data='parsSoobVk')],
    [InlineKeyboardButton(text='2️⃣ Парсинг беседы ВК', callback_data='InDev'
                                                                      '')], #parsBesedVk
    [InlineKeyboardButton(text='⬅️ НАЗАД', callback_data='backToStart')]
])


#КНОПКА ПАРСИНГ СООБЩЕСТВА ВК
soobPars = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⬅️ НАЗАД', callback_data='backParsChoosePars')]
])


#КНОПКА ПАРСИНГ БЕСЕДЫ ВК
besedPars = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⬅️ НАЗАД', callback_data='backParsChoosePars')]
])


#КНОПКА ИНСТРУКЦИЯ
instruction = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='❓️ Как получить токен', callback_data='getToken')],
    [InlineKeyboardButton(text='❓️ Видео-инструкция', url='https://www.youtube.com/watch?v=44CdUId13cw&ab_channel=myfilms_tv')],
    [InlineKeyboardButton(text='⬅️ НАЗАД', callback_data='backToStart')]

])


#КНОПКА ПОЛУЧИТЬ ТОКЕН
getToken = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⬅️ НАЗАД', callback_data='backToInstruction')]

])


#КНОПКИ О НАС
backToStart = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="⬅️ НАЗАД", callback_data='backToStart')]
])


#УБРАТЬ СООБЩЕНИЕ
autoDelMsg = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='❌', callback_data='deleteMe')]
])


#ПРОДОЛЖИТЬ В ЗАДАНИЯ
continueToTask = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="ПРОДОЛЖИТЬ ➡️", callback_data='backToRass')]

])