from pyrogram import Client, filters
from pyrogram.types import Message
from database.cleanservice_db import (
    enable_cleanservice,
    disable_cleanservice,
    is_cleanservice
)

@Client.on_message(filters.command("cleanservice") & filters.group)
async def cleanservice_toggle(client, message: Message):

    chat_id = message.chat.id
    user_id = message.from_user.id

    # Admin check
    member = await client.get_chat_member(chat_id, user_id)

    if member.status not in ["administrator", "creator"]:
        return await message.reply_text(
            "❌ Only admins can use this command."
        )

    status = await is_cleanservice(chat_id)

    if status:
        await disable_cleanservice(chat_id)

        await message.reply_text(
            "🧹 Clean Service ❌ Disabled"
        )

    else:
        await enable_cleanservice(chat_id)

        await message.reply_text(
            "🧹 Clean Service ✅ Enabled"
        )
