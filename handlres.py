import asyncio
import re
import os
import vk_api
from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.database import *
import app.keyboards as kb
from app.state import *



router = Router()






#КОМАНДА СТАРТ
users_count = 0
@router.message(CommandStart())
async def cmdStart(message: Message):
    global users_count
    users_count+=1
    start_msg = await message.answer('<b>Выберите операцию:</b>', reply_markup=kb.start, parse_mode='html')
    await message.delete()






@router.message(Command("status", prefix="!/"))
async def cmdStatus(message: Message):
    global users_count
    # Отправляем сообщение о текущем количестве пользователей
    await message.answer(f"<u>Количество пользователей</u>: <code>{users_count}</code>", reply_markup=kb.autoDelMsg, parse_mode='html')
    await message.delete()





#ПРОФИЛЬ
@router.callback_query(F.data == 'profile')
async def sendProfile(callback: CallbackQuery):
    username = callback.from_user.username
    user_id = callback.from_user.id
    vipStatus = "Нет"
    await callback.message.edit_text(f"<b>👤Ваш ник-нейм: <u>{username}</u>"
                                     f"\n🤖 Ваш цифровой ID: <u>{user_id}</u>"
                                     f"\n💎 VIP Статус: <u>{vipStatus}</u></b>",
                                     reply_markup=kb.profile, parse_mode='html')





#АККАУНТЫ
@router.callback_query(F.data == 'accounts')
async def sendAccounts(callback: CallbackQuery):
    global PustAcc
    user_id = callback.from_user.id
    token = await get_token_from_database(user_id)
    if token:
        authroz = vk_api.VkApi(token=token)
        vk = authroz.get_api()
        user_info = vk.users.get(fields='first_name,last_name')[0]
        user_first_n = user_info['first_name']
        user_last_n = user_info['last_name']
        await callback.message.edit_text(f"👤 <b>{user_first_n} {user_last_n}</b>", reply_markup=kb.accounts,
                                         parse_mode='html')
    else:
        await callback.message.edit_text("<b>Список аккаунтов пуст:</b>", reply_markup=kb.accounts, parse_mode='html')


SendToken = None

#ДОБАВИТЬ АККАУНТ
@router.callback_query(F.data == 'addAcc')
async def sendGetAccounts(callback: CallbackQuery, state: FSMContext):
    global SendToken
    await state.set_state(Auth.token)
    SendToken = await callback.message.edit_text("<b>Введите ссылку с токеном: \n\n"
                                                 "Для получение токена:"
                                                 "\n1) Зайдите <a href=vkhost.github.io>СЮДА</a>"
                                                 "\n2) Выбирите тип <i>VK Admin</i>"
                                                 "\n3) Нажмите кнопку <i>РАЗРЕШИТЬ</i>"
                                                 "\n4) Скопируйте ссылку сайта на которую вы были перенаправлены и скиньте ее боту!\n<u>ГОТОВО</u></b>",
                                                 reply_markup=kb.addAccount, parse_mode='html',
                                                 disable_web_page_preview=True)


@router.message(Auth.token)
async def getTokenAndAuth(message: Message, state: FSMContext):
    token_text = message.text
    global SendToken
    # получение токена из ссылки пользователя
    token_match = re.search(r'token=(.*?)&expires_in', token_text)
    if token_match:
        token = token_match.group(1)
        await state.update_data(token=token)
        await state.clear()
        user_id = message.from_user.id

        existing_token = await get_token_from_database(user_id)
        if existing_token:
            await message.delete()
            SendToken = await message.answer(
                "Хотите больше аккаунтов? Перейдите на VIP уровень привилегий уже сегодня и разблокируйте доступ к дополнительным аккаунтам ❕",
                parse_mode='html')
            await asyncio.sleep(5)
            await SendToken.delete()
            return

        insert_into_db = await insert_token_into_database(user_id, token)
        if insert_into_db:
            try:
                vk_auth = vk_api.VkApi(token=token)
                vk = vk_auth.get_api()
                user_info = vk.users.get()
                first_name = user_info[0]['first_name']
                last_name = user_info[0]['last_name']
                await SendToken.edit_text(f"👤 <b>{first_name} {last_name}</b>", reply_markup=kb.accounts,
                                          parse_mode='html')
                await message.delete()
                SuccessMsg = await message.answer(
                    f'Аккаунт <b>{first_name}</b>  <b>{last_name}</b> успшено добавлен ✔️', parse_mode='html')
                await asyncio.sleep(3)
                await SuccessMsg.delete()
            except vk_api.AuthError as e:
                await message.answer(f'Произошла ошибка при авторизации под данному токену!')
        else:
            await message.answer('Произошла ошибка при добавление данных в базу данных!')
    else:
        await message.answer("Не правильный формат ссылки!\nПопробуйте еще раз")

#УДАЛИТЬ АККАУНТ
@router.callback_query(F.data == 'delAcc')
async def delAcc(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    token = await get_token_from_database(user_id)
    if token:
        authroz = vk_api.VkApi(token=token)
        vk = authroz.get_api()
        user_info = vk.users.get(fields='first_name,last_name')[0]
        user_first_n = user_info['first_name']
        user_last_n = user_info['last_name']
        await state.set_state(Auth.deleteAcc)
        await delete_token_from_database(user_id)
        await callback.message.edit_text("<b>Список аккаунтов пуст:</b>", reply_markup=kb.accounts, parse_mode='html')
        await callback.answer(f"Аккаунт {user_first_n} {user_last_n} удален!", show_alert=True)
        await state.clear()
    else:
        await callback.answer("Аккаунт для удаления не найден!", show_alert=True)



@router.callback_query(F.data == 'task')
async  def getTask(callback: CallbackQuery):
    await callback.message.edit_text('<b>Выберите операцию:</b>', reply_markup=kb.chooseTask, parse_mode='html')





# РАССЫЛКА
@router.callback_query(F.data == 'rassilka')
async def sendRassilka(callback: CallbackQuery):
    await callback.message.edit_text('<b>Выберите операцию:</b>', reply_markup=kb.chooseRassilka, parse_mode='html')


# РАССЫЛКА ПО ЧАТАМ
chat_titles = []  # Создаем пустой список для хранения имен бесед


@router.callback_query(F.data == 'RassInChats')
async def sendMessageForVk(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Auth.SendMsg)
    user_id = callback.from_user.id
    token = await get_token_from_database(user_id)

    if token:
        authroz = vk_api.VkApi(token=token)
        vk = authroz.get_api()
        user_info = vk.users.get(fields='first_name,last_name')[0]
        user_first_n = user_info['first_name']
        user_last_n = user_info['last_name']

        # try:
        #     conversations = vk.messages.getConversations(extended=True)
        #
        #     global chat_titles
        #
        #     # Очищаем список перед добавлением новых имен
        #     chat_titles.clear()
        #
        #     # Вывод имен участников бесед и добавление имен в список
        #     for conv in conversations['items']:
        #         conv_data = conv['conversation']
        #         if conv_data['peer']['type'] == 'chat':
        #             chat_info = conv_data['chat_settings']
        #             if 'kicked' in chat_info and chat_info['kicked']:
        #                 continue
        #             if 'left' in chat_info and chat_info['left']:
        #                 continue
        #             chat_title = chat_info['title']
        #             chat_titles.append(chat_title)  # Добавляем имя беседы в список
        #
        #     keyboard = InlineKeyboardBuilder()
        #     for chat in chat_titles:
        #         keyboard.add(InlineKeyboardButton(text=chat, callback_data='erf'))
        #     keyboard.add(InlineKeyboardButton(text="⬅️ НАЗАД", callback_data="backToRass"))
        #     keyboard_markup = keyboard.adjust(1).as_markup()

        await callback.message.edit_text(
            f'<b>Отправьте сообщение, которое вы хотите отправить во все беседы ВК, используя аккаунт:👤 <u>{user_first_n} {user_last_n}</u></b>',
            reply_markup=kb.rassilkaInChats, parse_mode='html')

        # except Exception :
        #         pass
    else:
        await callback.message.edit_text(
            '<b>Для того, чтобы воспользоваться функцией <u>РАССЫЛКА ПО ЧАТАМ</u>, добавьте аккаунт в разделе <code>Профиль</code>-><code>Аккаунты</code></b>',
            reply_markup=kb.chooseTask, parse_mode='html')


@router.message(Auth.SendMsg)
async def messageSendIntVk(message: Message, state: FSMContext):
    text_for_send_into_vk = message.text
    full_message = f"{text_for_send_into_vk}\n\nЭтот текст бесплатно и автоматически отправляет телеграм бот - t.me/yankee_agency_bot"
    await message.delete()
    await state.update_data(SendMsg=full_message)
    user_id = message.from_user.id
    token = await get_token_from_database(user_id)
    if token:
        vk_auth = vk_api.VkApi(token=token)
        vk = vk_auth.get_api()

        # Отправляем сообщение о начале отправки с анимацией точек
        sending_message = await message.answer('<b>Процесс запущен.</b>', parse_mode='html')
        for i in range(3):
            await sending_message.edit_text(f'<b>Процесс запущен</b>{"." * (i + 1)}\u2063', parse_mode='html')
            await asyncio.sleep(1)
            await state.clear()

        chats = vk.messages.getConversations(filter='chats')['items']
        for chat in chats:
            chat_id = chat['conversation']['peer']['id']
            try:
                await asyncio.sleep(2)
                vk.messages.send(peer_id=chat_id, message=full_message, random_id=0)
            except:
                pass
        await sending_message.edit_text(f'Сообщение: <i><u>{text_for_send_into_vk}</u></i>\nУспшено отправлено во все беседы! 🚀',
            reply_markup=kb.autoDelMsg, parse_mode='html')


# РАССЫЛКА В ЛС
@router.callback_query(F.data == 'RassInLs')
async def sendRassInLs(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    token = await get_token_from_database(user_id)
    if token:
        authroz = vk_api.VkApi(token=token)
        vk = authroz.get_api()
        await state.set_state(Rass.linksForRas)
        msg = await callback.message.edit_text(
            '<b>Вставьте ссылки на акканты пользователей ВК <u>10 ссылок макс. 📌</u>\n\n'
            '⚠️ Убедитесь, что ссылки ведут на открытые аккаунты. Закрытые аккаунты не получат рассылку </b>',
            reply_markup=kb.rassilkaInLs, parse_mode='html')
        await state.update_data(text_message_id=msg.message_id)
    else:
        await callback.message.edit_text(
            '<b>Для того, чтобы воспользоваться функцией <u>РАССЫЛКА В ЛС</u>, добавьте аккаунт в разделе <code>Профиль</code>-><code>Аккаунты</code></b>',
            reply_markup=kb.chooseTask, parse_mode='html')


@router.message(Rass.linksForRas)
async def gotLinksForRass(message: Message, state: FSMContext):
    links_text = message.text
    user_id = message.from_user.id
    if links_text.count('\n') + 1 > 10:  # Проверяем количество ссылок
        data = await state.get_data()
        text_message_id = data.get("text_message_id")
        await message.bot.edit_message_text(chat_id=message.chat.id, message_id=text_message_id,
                                            text="<b>Пожалуйста, приобретите <u>VIP Статус</u> для отправки более 10 ссылок!</b>",
                                            parse_mode='html', reply_markup=kb.rassilkaInLs)
        await message.delete()
        return

    await state.update_data(linksForRas=message.text)
    await message.delete()

    data = await state.get_data()
    text_message_id = data.get("text_message_id")
    await message.bot.edit_message_text(chat_id=message.chat.id, message_id=text_message_id,
                                        text="<b>Введите текст сообщения:</b> ", parse_mode='html',
                                        reply_markup=kb.rassilkaInLs)
    await state.set_state(Rass.msgForRas)


@router.message(Rass.msgForRas)
async def send_msg_in_ls(message: Message, state: FSMContext):
    await state.update_data(msgForRas=message.text)
    await message.delete()
    user_id = message.from_user.id
    token = await get_token_from_database(user_id)
    data = await state.get_data()
    text_message_id = data.get("text_message_id")
    accsForRass = data["linksForRas"]
    msg = data["msgForRas"]
    full_message = f"{msg}\n\nЭтот текст бесплатно и автоматически отправляет бот - t.me/yankee_agency_bot"

    if token:
        authroz = vk_api.VkApi(token=token)
        vk = authroz.get_api()
        user_info = vk.users.get(fields='first_name,last_name')[0]
        user_first_n = user_info['first_name']
        user_last_n = user_info['last_name']
        ssilki = re.findall(r'https://vk.com/([^/\s]+)', accsForRass)
        if len(accsForRass.split('\n')) == 1 and 'https://' in accsForRass:
            await state.clear()
            await message.bot.edit_message_text(chat_id=message.chat.id, message_id=text_message_id,
                                                text="<b>Рассылка завершена успешно! 🎉</b>",
                                                parse_mode='html', reply_markup=kb.chooseTask)
            for username in ssilki:
                try:
                    user_info = vk.users.get(user_ids=username)
                    user_id = user_info[0]['id']
                    vk.messages.send(user_id=user_id, message=full_message, random_id=0)
                    await asyncio.sleep(1)
                except Exception as e:
                    pass
        else:
            await message.bot.edit_message_text(chat_id=message.chat.id, message_id=text_message_id,
                                                text=f"<b>Рассылка запущена 📨\nПользователи получат сообщения с промежутком в 20 минут\nИспользуемый аккаунт:👤 <u>{user_first_n} {user_last_n}</u></b>",
                                                parse_mode='html', reply_markup=kb.continueToTask)
            await state.clear()
            for username in ssilki:
                try:
                    user_info = vk.users.get(user_ids=username)
                    user_id = user_info[0]['id']
                    vk.messages.send(user_id=user_id, message=full_message, random_id=0)
                    await asyncio.sleep(1200)
                except Exception as e:
                    pass
            await message.answer("<b>Рассылка завершена успешно! 🎉</b>",
                                 parse_mode='html', reply_markup=kb.autoDelMsg)

    else:
        await message.answer("<u>ОШИБКА БАЗЫ ДАННЫХ ОБРАТИТЕСЬ В ПОДДЕРЖКУ!</u>", parse_mode='html')





# VIP
@router.callback_query(F.data == 'vip')
async def getVip(callback: CallbackQuery):
    await callback.message.edit_text("<b>GOLD VIP 👇🏻"
                                     "\n• Возможность добавить 3+ аккаунтов"
                                     "\n• Пиар в 15+ чатах"
                                     "\n• Рассылка на 30+ аккаунтов в ЛС"
                                     "\n• Отсутствие нашей рекламы в вашем тексте"
                                     "\n• Неограниченный Парсинг"
                                     "\n• Неограниченный пиар"
                                     "\nСтоимость - 90₽"
                                     "\nПополнение доступно на: Cryptobot, Тинькофф, Сбербанк, СБП</b>",
                                     reply_markup=kb.vip, parse_mode='html')





#МАГАЗИН
@router.callback_query(F.data == 'shop')
async def getShop(callback: CallbackQuery):
    await callback.message.edit_text("👥 <b>Приобрести аккаунт VK/TELEGRAM - от 50₽"
                                     "\n💭 Приобрести базу чатов/бесед - от 50₽"
                                     "\n🧑‍🧑‍🧒‍🧒 Накрутка Telegram/VK/TikTok/Youtube и др. - от 0,1 коп"
                                     "\n🤖 Авторассылка ( настройка и прочее на нас ) - от 100₽"
                                     "\n<u>Связь</u> - @nobioyetj</b>", reply_markup=kb.shop, parse_mode='html')





#ПАРСЕР
@router.callback_query(F.data == 'parser')
async def sendParsChoosePars(callback: CallbackQuery):
    await callback.message.edit_text('<b>Выберите тип парсинга:</b>', reply_markup=kb.chooseParsing, parse_mode='html')





#ПАРСИНГ СООБЩЕСТВО ВК
@router.callback_query(F.data == 'parsSoobVk')
async def sendParsSoobVk(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Pars.vkSoob)
    await callback.message.edit_text('⚙️<b> ПАРСЕР ВК СООБЩЕСТВО ⚙️'
                                     '\n\nПолучайте ссылки на пользователей из любого сообщество ВКонтакте с легкостью!</b>\n\n'
                                     '<u>Просто введите ссылку на сообщество и получите результат</u>:',
                                     reply_markup=kb.soobPars, parse_mode='html')


@router.message(Pars.vkSoob)
async def getVkSoobData(message: Message, state: FSMContext):
    from_user_soob_link = message.text
    if from_user_soob_link.startswith("https://vk.com/"):
        soobLink = from_user_soob_link.split("https://vk.com/")[1]
        user_id = message.from_user.id
        token = await get_token_from_database(user_id)
        if token:
            authroz = vk_api.VkApi(token=token)
            vk = authroz.get_api()
            group_id = soobLink
            try:
                get_member = vk.groups.getMembers(group_id=group_id, count=10, fields='first_name,last_name')

                member_list = []

                for member in get_member['items']:
                    user_first_n = member['first_name']
                    user_last_n = member['last_name']
                    user_id = member['id']

                    member_list.append(f"https://vk.com/id{user_id}")

                # Отправляем все данные одним сообщением
                await message.answer('\n'.join(member_list), reply_markup=kb.autoDelMsg, disable_web_page_preview=True)
                await message.delete()
                await state.clear()
            except Exception:
                await message.answer("<b>⚠️ Отправленное вами сообщество, скрыло информацию о подписчиках. \n\nОтправьте сообщество в котором подписчики не скрыты</b>", reply_markup=kb.autoDelMsg, parse_mode='html')
                await state.clear()
                await message.delete()

        else:
            await message.answer("Добавьте аккаунт и повторите попытку, пожалуйста")
    else:
        await message.answer("Извините, но ссылка выглядит неправильно 🚫\n ")




#ПАРСИНГ БЕСЕДЫ ВК
@router.callback_query(F.data == 'parsBesedVk')
async def sendParsBesedVk(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Pars.vkBesed)
    await callback.message.edit_text('<b>⚙️ ПАРСЕР ВК БЕСЕД ⚙️'
                                     '\n\nПолучайте ссылки на пользователей из любой беседы ВКонтакте с легкостью!</b>\n\n'
                                     '<u>Просто введите ссылку на беседу и получите результат</u>:',
                                     reply_markup=kb.besedPars, parse_mode='html')


@router.message(Pars.vkBesed)
async def getParsBesedVk(message: Message):
    from_user_besed_link = message.text
    await message.delete()

    if from_user_besed_link.startswith("https://vk.com/im?sel=c"):
        user_id = message.from_user.id
        token = await get_token_from_database(user_id)
        if token:
            authroz = vk_api.VkApi(token=token)
            vk = authroz.get_api()

            besedaId = re.search(r'sel=c(\d+)', from_user_besed_link).group(1)
            participants = vk.messages.getChatUsers(chat_id=besedaId, fields='nickname')

            participants = participants[:10]
            account_links = []
            for participant in participants:
                # Формирование ссылки на аккаунт участника
                account_link = 'https://vk.com/id{}'.format(participant['id'])
                account_links.append(account_link)
            await message.answer("\n".join(account_links), reply_markup=kb.autoDelMsg,  disable_web_page_preview=True)
        else:
            await message.answer("Добавьте аккаунт и повторите попытку, пожалуйста")
    else:
        await message.answer("Извините, но ссылка выглядит неправильно 🚫\n")





#ИНСТРУКЦИЯ
@router.callback_query(F.data == 'instruction')
async def sendInstruction(callback: CallbackQuery):
    await callback.message.edit_text('<b>Выберите операцию:</b>', reply_markup=kb.instruction, parse_mode='html', disable_web_page_preview=True)




#ПОЛУЧИТЬ ТОКЕН
@router.callback_query(F.data == 'getToken')
async def getToken (callback: CallbackQuery):
    await callback.message.edit_text('<b>Для получение токен</b> '
                                      '\n1) Зайдите <a href=vkhost.github.io>СЮДА</a> '
                                      '\n2) Выбирите тип <i>VK Admin</i> '
                                      '\n3) Нажмите кнопку <i>РАЗРЕШИТЬ</i> '
                                      '\n4) Скопируйте ссылку сайта на которую вы были перенаправлены и скиньте ее боту! '
                                      '\n<b>ГОТОВО</b>',
                                      reply_markup=kb.getToken, parse_mode='html', disable_web_page_preview=True)









#О НАС
@router.callback_query(F.data == 'aboutUs')
async def  sendAboutUs(callback: CallbackQuery):
    await callback.message.edit_text("👋 <u>Добро пожаловать!"
                                     "\n\n🚀</u> Присоединяйтесь к нашему каналу - <a href='https://t.me/yankeeagency'>Yankee Agency</a>, чтобы быть в курсе свежих новостей!"
                                     "\n\n🛠️ Нужна помощь или вопросы? Обращайтесь в @nobioyetj для технической поддержки. 💬",
        reply_markup=kb.backToStart, parse_mode='html', disable_web_page_preview=True)




@router.callback_query(F.data == 'backToStart')
async def backToStart(callback: CallbackQuery):
    await callback.message.edit_text('<b>Выберите операцию:</b>', reply_markup=kb.start, parse_mode='html')


@router.callback_query(F.data == 'backToPrfl')
async def backToPrfl(callback: CallbackQuery):
    await sendProfile(callback)


@router.callback_query(F.data == 'backToInstruction')
async def backToInstruction(callback: CallbackQuery):
    await sendInstruction(callback)


@router.callback_query(F.data == 'backToAcc')
async def backToAcc(callback: CallbackQuery, state: FSMContext):
    await sendAccounts(callback)
    await state.clear()


@router.callback_query(F.data == 'backToTask')
async def backToTask(callback: CallbackQuery):
    await getTask(callback)


@router.callback_query(F.data == 'backToRass')
async def backToRass(callback: CallbackQuery, state: FSMContext):
    await sendRassilka(callback)
    await state.clear()

@router.callback_query(F.data == 'backParsChoosePars')
async def backToParsChoose(callback: CallbackQuery, state: FSMContext):
    await sendParsChoosePars(callback)
    await state.clear()



@router.callback_query(F.data == 'deleteMe')
async def deleteKeyboard(callback: CallbackQuery):
    await callback.message.delete()



@router.callback_query(F.data == 'InDev')
async def In_Dev(callback: CallbackQuery):
    await callback.answer('Кнопка в разработке !', show_alert=True)


