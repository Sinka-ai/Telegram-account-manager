import asyncio
import os
from contextlib import suppress
from TGConvertor.manager import SessionManager
from pathlib import Path
from pyrogram import filters, Client
import json
from commands import *
import random
import string

def display_banner():
    banner = """
    ███████╗██╗███╗   ██╗██╗  ██╗ █████╗     █████╗ ██╗
    ██╔════╝██║████╗  ██║██║ ██╔╝██╔══██╗   ██╔══██╗██║
    ███████╗██║██╔██╗ ██║█████╔╝ ███████║   ███████║██║
    ╚════██║██║██║╚██╗██║██╔═██╗ ██╔══██║   ██╔══██║██║
    ███████║██║██║ ╚████║██║  ██╗██║  ██║██╗██║  ██║██║
    ╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝

                 MADE BY sinka_ai
    """
    print(banner)

# Загрузка конфигурации
with open('config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)
    api_id = config["api_id"]
    api_hash = config["api_hash"]
    device_model = config['device_model']
    system_version = config['system_version']
    app_version = config['app_version']
    time_between = int(config['time_between'])
    message_for_spam = config['message_for_spam']
    bio_message = config.get('bio_message', '???')  # Получаем сообщение для био из конфига

use_config_message = True  # Переменная для выбора использования сообщения из конфига

def check_number(phone):
    with open('yw_numbers.txt', 'r') as file:
        numbers = [x.split('\n')[0] for x in file.readlines()]
    if phone in numbers:
        with open('repeats_numbers.txt', 'a') as file:
            file.write(f'{phone}\n')
        print(f'Аккаунт с номером {phone} уже был проверен')
        return 0
    else:
        with open('yw_numbers.txt', 'a') as file:
            file.write(f'{phone}\n')
        return 1

def pyrogram_session_from_tdata(path: str):
    try:
        session = SessionManager.from_tdata_folder(Path(path))
        app = session.pyrogram.client(session.api)
        app.APP_VERSION = app_version
        app.DEVICE_MODEL = device_model
        app.SYSTEM_VERSION = system_version
        app.api_hash = config["api_hash"]
        app.api_id = config["api_id"]
        return app
    except:
        return None

async def get_last_message(app: Client):
    try:
        async with app:
            async for message in app.get_chat_history('SpamBot', limit=1, offset_id=-1):
                return message.text
    except:
        return 'err'

async def remove_spam(path: str):
    client = pyrogram_session_from_tdata(path)
    is_valid = True
    if client == None:
        is_valid = None

    if client != None:
        try:
            async with client:
                user = await client.get_me()
                phone_number = user.phone_number
        except Exception as ex:
            is_valid = False
    else:
        print(f'{path} | НЕ ВАЛИД')

    if is_valid is not None and is_valid == True:
        print(f'{phone_number} | Начал...')
        try:
            async with client:
                await client.send_message("SpamBot", "/start")
        except Exception as e:
            print(f'{phone_number} | СПАМ')
            return

        await asyncio.sleep(3)
        last_message = await get_last_message(client)

        if 'Unfortunately' in last_message or 'afraid some Telegram':
            async with client:
                await client.send_message("SpamBot", "This is a mistake")
            print(f'{phone_number} | Отправил сообщение: This is a mistake')
            await asyncio.sleep(3)
            last_message = await get_last_message(client)
            if 'patience' in last_message:
                print("Аккаунт уже на проверке")
                return
            if 'you think the' in last_message:
                async with client:
                    await client.send_message("SpamBot", "Yes")
                print(f'{phone_number} | Отправил сообщение: Yes')
                await asyncio.sleep(3)
                last_message = await get_last_message(client)
                if 'Please confirm' in last_message:
                    async with client:
                        await client.send_message("SpamBot", "No! Never did that!")
                    print(f'{phone_number} | Отправил сообщение: No! Never did that!')
                    await asyncio.sleep(3)
                    last_message = await get_last_message(client)
                    if 'some details about' in last_message:
                        async with client:
                            if use_config_message:
                                await client.send_message("SpamBot", f"{message_for_spam}")
                                print(f'{phone_number} | Отправил сообщение: {message_for_spam}')
                            else:
                                random_message = generate_random_message()
                                await client.send_message("SpamBot", f"{random_message}")
                                print(f'{phone_number} | Отправил случайное сообщение: {random_message}')

                        await asyncio.sleep(3)
                        last_message = await get_last_message(client)
                        if 'submitted' in last_message:
                            print(f'{phone_number} | Заявка на снятие спама успешно отправлена')
                            move_folder_2(path, True, phone_number, spam_folder='снятие спама')
                            return
                        else:
                            print(f'{phone_number} | Не удалось отправить заявку на снятие спама')
                            move_folder_2(path, False, phone_number)
                            return
                    else:
                        print(f'{phone_number} | Не удалось отправить заявку на снятие спама')
                        move_folder_2(path, False, phone_number)
                        return
                else:
                    print(f'{phone_number} | Не удалось отправить заявку на снятие спама')
                    move_folder_2(path, False, phone_number)
                    return
            else:
                print(f'{phone_number} | Не удалось отправить заявку на снятие спама')
                move_folder_2(path, False, phone_number)
                return
        if 'Очень жаль' in last_message or 'К сожалению' in last_message:
            async with client:
                await client.send_message("SpamBot", "Это ошибка")
            print(f'{phone_number} | Отправил сообщение: Это ошибка')
            await asyncio.sleep(3)
            last_message = await get_last_message(client)
            if "терпение" in last_message:
                print("Заявка уже отправлена")
                return
            if 'Если Вы считаете' in last_message:
                async with client:
                    await client.send_message("SpamBot", "Да")
                print(f'{phone_number} | Отправил сообщение: Да')
                await asyncio.sleep(3)
                last_message = await get_last_message(client)
                if 'подтвердите' in last_message:
                    async with client:
                        await client.send_message("SpamBot", "Нет, ничего подобного не было.")
                    print(f'{phone_number} | Отправил сообщение: Нет, ничего подобного не было.')
                    await asyncio.sleep(3)
                    last_message = await get_last_message(client)
                    if 'расскажите' in last_message:
                        async with client:
                            if use_config_message:
                                await client.send_message("SpamBot", f"{message_for_spam}")
                                print(f'{phone_number} | Отправил сообщение: {message_for_spam}')
                            else:
                                random_message = generate_random_message()
                                await client.send_message("SpamBot", f"{random_message}")
                                print(f'{phone_number} | Отправил случайное сообщение: {random_message}')

                        print(f'{phone_number} | Отправил сообщение: {message_for_spam}')
                        await asyncio.sleep(3)
                        last_message = await get_last_message(client)
                        if 'отправлена' in last_message:
                            print(f'{phone_number} | Заявка на снятие спама успешно отправлена')
                            move_folder_2(path, True, phone_number)
                            return
                        else:
                            print(f'{phone_number} | Не удалось отправить заявку на снятие спама')
                            move_folder_2(path, False, phone_number)
                            return
                    else:
                        print(f'{phone_number} | Не удалось отправить заявку на снятие спама')
                        move_folder_2(path, False, phone_number)
                        return
                else:
                    print(f'{phone_number} | Не удалось отправить заявку на снятие спама')
                    move_folder_2(path, False, phone_number)
                    return
            else:
                print(f'{phone_number} | Не удалось отправить заявку на снятие спама')
                move_folder_2(path, False, phone_number)
                return
        move_folder(path, True, False, phone_number)
        print(f'{phone_number} | ВАЛИДНЫЙ, НЕ СПАМ')
        return

async def is_tdata_valid(path: str):
    client = pyrogram_session_from_tdata(path)
    is_valid = True
    if client is None:
        is_valid = None

    if client is not None:
        try:
            await asyncio.wait_for(check_account_is_ok(client, path), timeout=15)
            try:
                async with client:
                    user = await client.get_me()
                    phone_number = user.phone_number
                    check = check_number(phone_number)
                    if check == 0:
                        os.rmdir(path)
                        print(f'Аккаунт {phone_number} уже был проверен')
                        return
                    with suppress():
                        print(f'{phone_number} | Обновление био...')
                        await update_bio(client, bio_message)  # Добавляем параметр для био
                        print(f'{phone_number} | Настройки приватности...')
                        await change_privacy(client)
                        print(f'{phone_number} | Выход из диалогов...')
                        resu = await leave_dialogs(client, phone_number, path)
                        if resu == 2: return
            except:
                is_valid = False

        except asyncio.TimeoutError:
            print(f'{path} | Тайм-аут: НЕ ВАЛИДНЫЙ (время выполнения проверки превысило 40 секунд)')
            move_folder(path, False, True, 0)
            return
        except Exception as ex:
            if "404" in str(ex) or "auth key not found" in str(ex):
                print(f'{path} | НЕ ВАЛИДНЫЙ (auth key not found)')
                move_folder(path, False, True, 0)
                return
            else:
                print(f'Ошибка при обработке {path}: {str(ex)}')
            is_valid = False

    if is_valid is not None and is_valid == True:
        print(f'{phone_number} | Проверка на спам...')
        try:
            async with client:
                await client.send_message("SpamBot", "/start")
        except Exception as e:
            move_folder(path, True, True, phone_number)
            print(f'{phone_number} | ВАЛИДНЫЙ, СПАМ')
            return

        await asyncio.sleep(2)
        last_message = await get_last_message(client)
        if 'Telegram Premium' not in last_message and 'Unfortunately' not in last_message and 'Очень жаль' not in last_message and 'err' not in last_message:
            move_folder(path, True, False, phone_number)
            print(f'{phone_number} | ВАЛИДНЫЙ, НЕ СПАМ')
            return
        elif 'Пока действуют ограничения' in last_message or 'While the account is limited' in last_message or 'некоторые номера телефонов' in last_message or 'some phone numbers' in last_message:
            move_folder_2(path, False, phone_number, spam_folder='spam3')
            print(f'{phone_number} | Вечный спам блок')
            return
        else:
            move_folder_2(path, False, phone_number, spam_folder='spam1')
            print(f'{phone_number} | Временный спам блок')
            return
    elif is_valid is not None and is_valid == False:
        move_folder(path, False, True, 0)
        print(f'{path} | НЕ ВАЛИДНЫЙ')
        return
    move_folder(path, None, True, 0)
    print(f'{path} | НЕ УДАЛОСЬ ПРОВЕРИТЬ')
    return

async def check_account(client, path):
    async with client:
        user = await client.get_me()
        phone_number = user.phone_number
        check = check_number(phone_number)
        if check == 0:
            os.rmdir(path)
            print(f'Аккаунт {phone_number} уже был проверен')
            return
        with suppress():
            print(f'{phone_number} | Обновление био...')
            await update_bio(client, bio_message)
            print(f'{phone_number} | Настройки приватности...')
            await change_privacy(client)
            print(f'{phone_number} | Выход из диалогов...')
            resu = await leave_dialogs(client, phone_number, path)
            if resu == 2:
                return

async def check_account_is_ok(client, path):
    async with client:
        user = await client.get_me()
        phone_number = user.phone_number

def generate_random_message(length=10):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

async def main():
    all_tdata = get_folder_names()
    for tdata in all_tdata:
        location = f'accounts/{tdata}'
        print(f'Проверяю {location}')
        await is_tdata_valid(location)
        await asyncio.sleep(time_between)

async def ban_remove():
    all_tdata = get_folder_names_2('spam2')
    for tdata in all_tdata:
        location = f'spam2/{tdata}'
        print(f'Снимаю {location}')
        await remove_spam(location)
        await asyncio.sleep(time_between)

def main_1():
    display_banner()
    global use_config_message  # Указываем что будем использовать глобальную переменную

    print(
        f'\nВаши настройки: \nAPI_ID: {api_id}\nAPI_HASH: {api_hash}\nDevice model: {device_model}\nApp version: {app_version}\nSystem version: {system_version}\nTime between: {time_between} sec.\nMessage for spam: {message_for_spam}\nBio message: {bio_message}\n'
    )

    while True:
        ask = input('Выберите:\n1. Чекер аккаунтов\n2. Снятие спама\n- ')
        if ask not in '12':
            continue
        else:
            method = int(ask)
            break

    if method == 2:
        while True:
            ask_message = input('Использовать сообщение из конфига? (да/нет): ')
            if ask_message.lower() == 'да':
                use_config_message = True
                break
            elif ask_message.lower() == 'нет':
                use_config_message = False
                break
            else:
                print('Введите "да" или "нет".')

    if method == 1:
        asyncio.run(main())
    else:
        asyncio.run(ban_remove())

while True:
    main_1()
