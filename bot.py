from aiogram import Dispatcher, Bot, types
from aiogram.types import Message
from aiogram.filters import Command
import asyncio
import whois
import socket
from datetime import datetime


bot = Bot(token="")  
dp = Dispatcher()


def format_date(date):
    """Форматує дату у вигляді DD.MM.YYYY"""
    if isinstance(date, list): 
        date = date[0]
    if isinstance(date, datetime):
        return date.strftime("%d.%m.%Y")
    return "N/A"


def get_domain_info(domain_name: str):
    try:
        ip = socket.gethostbyname(domain_name)
        w = whois.whois(domain_name)
        creation_date = format_date(w.get("creation_date"))        
        name_servers = w.get("name_servers", [])
        if isinstance(name_servers, str):
            name_servers = [name_servers]
        ns_formatted = "\n".join(f"{i+1}. {ns}" for i, ns in enumerate(name_servers)) if name_servers else "N/A"
        info = (
            f"```\n"
            f"Domain Name: {w.get('domain_name', 'N/A').lower()}\n"
            f"IP-адреса: {ip}\n"
            f"Creation Date: {creation_date}\n"
            f"Імя: {w.get('registrar', 'N/A')}\n"
            f"Місцезнаходження: {w.get('country', 'N/A')}, {w.get('state', 'N/A')}\n"
            f"Name Servers:\n{ns_formatted}\n"
            f"```"
        )

        return info
    except Exception as e:
        return f"Error: {e}"


@dp.message()
async def whois_lookup(message: Message):
    domain_name = message.text.strip()

    if not domain_name:
        
        return

    info = get_domain_info(domain_name)
    await message.answer(info, parse_mode="MarkdownV2")



async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
