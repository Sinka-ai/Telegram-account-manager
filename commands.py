from pyrogram import Client
from pyrogram.raw import functions
from pyrogram.raw.functions.messages import DeleteHistory
from pyrogram.raw.types import InputPrivacyKeyPhoneNumber, InputPrivacyValueAllowAll
from data import *
from pyrogram.raw.functions.messages import DeleteMessages

async def update_bio(client: Client, bio_message):
    await client.update_profile(bio=bio_message)

async def leave_dialogs(client: Client, phone, path):
    with open('usernames.txt', 'r') as file:
        users = file.readlines()
    usernames = [user.split('\n')[0][1:] for user in users]
    async for dialog in client.get_dialogs(limit=10000000):
        try:
            if dialog.chat.username in usernames:
                print(f'Аккаунт с номером {phone} перенесен в папку accounts2')
                move_folder_3(path, phone)
                return 2
            await dialog.chat.leave()
            peer = await client.resolve_peer(dialog.chat.id)
            await client.invoke(DeleteHistory(max_id=0, peer=peer, just_clear=True, revoke=1))
            await client.leave_chat(dialog.chat.id, delete=True)
        except Exception as e:
            pass

async def change_privacy(client: Client):
    await client.invoke(
        functions.account.SetPrivacy(
            key=InputPrivacyKeyPhoneNumber(), rules=[InputPrivacyValueAllowAll()]
        )
    )
