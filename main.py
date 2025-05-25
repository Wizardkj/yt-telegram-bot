import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
import yt_dlp

from dotenv import load_dotenv
load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.reply("Привіт! Надішли мені посилання на YouTube відео, і я скачаю його для тебе!")

@dp.message_handler()
async def download_youtube(message: Message):
    url = message.text.strip()
    if "youtube.com" not in url and "youtu.be" not in url:
        await message.reply("Це не схоже на YouTube посилання.")
        return

    await message.reply("🔄 Завантажую відео...")

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'download.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'noplaylist': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        with open("download.mp3", "rb") as audio:
            await message.reply_audio(audio, title="Твоє MP3", performer="YouTube Bot")
        os.remove("download.mp3")

    except Exception as e:
        await message.reply(f"Сталася помилка 😢: {e}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
