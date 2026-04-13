# database/cleanservice_db.py

from database.users_chats_db import db

async def enable_cleanservice(chat_id):
    await db.update_one(
        {"chat_id": chat_id},
        {"$set": {"cleanservice": True}},
        upsert=True
    )

async def disable_cleanservice(chat_id):
    await db.update_one(
        {"chat_id": chat_id},
        {"$set": {"cleanservice": False}},
        upsert=True
    )

async def is_cleanservice(chat_id):
    data = await db.find_one({"chat_id": chat_id})
    
    if not data:
        return False

    return data.get("cleanservice", False)
