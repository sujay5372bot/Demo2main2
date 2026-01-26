import requests
import base64
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


def follow_redirects(url: str):
    headers = {"User-Agent": "Mozilla/5.0 (BypassBot)"}
    r = requests.get(url, headers=headers, allow_redirects=True, timeout=20)
    return r.url


@Client.on_message(filters.command("bypass"))
def bypass_handler(client, message: Message):

    shortlink = None

    # Case 1: /bypass <link>
    if len(message.command) > 1:
        shortlink = message.command[1]

    # Case 2: /bypass reply to a message that contains link
    elif message.reply_to_message:
        shortlink = message.reply_to_message.text

    # Case 3: /bypass ke baad user ne link next line me bheja
    elif message.text and "\n" in message.text:
        parts = message.text.split("\n")
        if len(parts) > 1:
            shortlink = parts[1].strip()

    if not shortlink:
        return message.reply(
            "❌ Link nahi mila.\n\nUse:\n"
            "`/bypass <link>`\n\n"
            "Ya kisi link ko reply karke `/bypass` bhejo."
        )

    msg = message.reply("🔄 Bypassing link...")

    try:
        final_url = special_bypass(shortlink)
        if not final_url:
            final_url = follow_redirects(shortlink)

        msg.edit(
            f"🔓 **Bypassed Successfully!**\n\n"
            f"➡️ `{final_url}`"
        )
    except Exception as e:
        msg.edit("❌ Bypass failed! Link protected ya error aaya.")
