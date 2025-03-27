import telebot
import os
from pytube import YouTube
from pytube.exceptions import VideoUnavailable, RegexMatchError

API_TOKEN = os.environ.get("API_TOKEN")

proxies = {"http": "http://127.0.0.1:10808", "https": "http://127.0.0.1:10808"}

bot = telebot.TeleBot(API_TOKEN)


def download_video(url):
    try:
        yt = YouTube(url, proxies=proxies, use_oauth=False, allow_oauth_cache=True)
        yt.check_availability()
        stream = (
            yt.streams.filter(progressive=True, file_extension="mp4")
            .order_by("resolution")
            .desc()
            .first()
        )
        if not stream:
            return None
        output_path = os.path.join(os.getcwd(), "videos")
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        return stream.download(output_path=output_path)
    except (VideoUnavailable, RegexMatchError, Exception):
        return None


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, f"سلام {message.chat.first_name} لینک ویدیو را ارسال کنید.")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        if not message.text.startswith(("http://", "https://", "youtu")):
            bot.reply_to(message, "لطفا لینک معتبر ارسال کنید")
            return

        video_path = download_video(message.text)

        if video_path:
            with open(video_path, "rb") as video_file:
                bot.send_video(message.chat.id, video_file)
            os.remove(video_path)
        else:
            bot.reply_to(message, "خطا در دانلود ویدیو")

    except Exception as e:
        bot.reply_to(message, "خطای سیستمی رخ داد")


if __name__ == "__main__":
    if not os.path.exists("videos"):
        os.makedirs("videos")
    bot.infinity_polling()
