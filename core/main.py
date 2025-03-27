import telebot
import os
from telebot import types
from pytube.download_helper import (
    download_videos_from_channels,
    download_video,
    download_videos_from_list,
)

API_TOKEN = os.environ.get("API_TOKEN")

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(
        message,
        f"سلام {message.chat.first_name} به ربات تست پایتون خوش آمدید! در این ربات شما می توانید پس از start با فرستادن لینک ویدیو های یوتیوب آن ها را دانلود کنید.",
    )


bot.infinity_polling()
