#SUJAY 😎
import requests
from pyrogram import filters
from pyrogram.types import Message
from urllib.parse import urlparse, parse_qs, unquote
import base64

from pyrogram import Client     # Agar tumhara Client object 'app' ya 'bot' name se hai

def special_bypass(url: str):
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    host = parsed.netloc.lower()

    # t.me redirect
    if "t.me" in host and "url" in qs:
        return unquote(qs["url"][0])

    # gplinks.in
    if "gplinks" in host:
        if "url" in qs:
            return unquote(qs["url"][0])
        if "id" in qs:
            try:
                return base64.b64decode(qs["id"][0]).decode()
            except:
                pass

    # Adfly
    if "adf.ly" in host or "adfly" in host:
        if "url" in qs:
            return unquote(qs["url"][0])

    # Droplink
    if "droplink" in host:
        if "url" in qs:
            return unquote(qs["url"][0])

    return None

def follow_redirects(url: str):
    headers = {"User-Agent": "Mozilla/5.0 (BypassBot)"}
    r = requests.get(url, headers=headers, allow_redirects=True, timeout=20)
    return r.url

@Client.on_message(filters.command("bypass") & filters.private)
def bypass_handler(client, message: Message):
    if len(message.command) < 2:
        return message.reply("❌ Use: /bypass <link>")

    shortlink = message.command[1].strip()
    msg = message.reply("🔄 Bypassing link...")

    try:
        final_url = special_bypass(shortlink)
        if not final_url:
            final_url = follow_redirects(shortlink)

        msg.edit(
            f"🔓 **Bypassed!**\n\n➡️ `{final_url}`"
        )
    except Exception as e:
        msg.edit("❌ Bypass failed!")
