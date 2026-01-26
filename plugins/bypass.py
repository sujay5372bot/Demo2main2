import requests
import base64
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from urllib.parse import urlparse, parse_qs, unquote

def special_bypass(url: str):
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    host = parsed.netloc.lower()

    if "t.me" in host and "url" in qs:
        return unquote(qs["url"][0])

    if "gplinks" in host:
        if "url" in qs:
            return unquote(qs["url"][0])
        if "id" in qs:
            try:
                return base64.b64decode(qs["id"][0]).decode()
            except:
                pass

    if "adf.ly" in host or "adfly" in host:
        if "url" in qs:
            return unquote(qs["url"][0])

    if "droplink" in host:
        if "url" in qs:
            return unquote(qs["url"][0])

    return None


def follow_redirects_sync(url: str):
    headers = {"User-Agent": "Mozilla/5.0 (BypassBot)"}
    r = requests.get(url, headers=headers, allow_redirects=True, timeout=20)
    return r.url


async def follow_redirects(url: str):
    # blocking requests ko async me chalane ke liye
    return await asyncio.to_thread(follow_redirects_sync, url)


@Client.on_message(filters.command("bypass"))
async def bypass_handler(client, message: Message):

    shortlink = None

    # /bypass <link>
    if len(message.command) > 1:
        shortlink = message.command[1]

    # reply me link ho
    elif message.reply_to_message and message.reply_to_message.text:
        shortlink = message.reply_to_message.text.strip()

    # multiline
    elif message.text and "\n" in message.text:
        parts = message.text.split("\n")
        if len(parts) > 1:
            shortlink = parts[1].strip()

    if not shortlink:
        return await message.reply_text(
            "❌ Link nahi mila.\n\n"
            "Use:\n"
            "`/bypass <link>`\n\n"
            "Ya kisi link par reply karke `/bypass` bhejo."
        )

    msg = await message.reply_text("🔄 Bypassing link...")

    try:
        final_url = special_bypass(shortlink)
        if not final_url:
            final_url = await follow_redirects(shortlink)

        await msg.edit_text(
            f"🔓 **Bypassed Successfully!**\n\n"
            f"➡️ `{final_url}`"
        )
    except Exception as e:
        await msg.edit_text("❌ Bypass failed! Link protected ya error aaya.")
