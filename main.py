import os
import telebot
from moviepy.editor import VideoFileClip
from pytube import YouTube
from telebot import types

# Constants
INPUT_VIDEO = 0
INPUT_LINK = 0

# Initialize the bot with your token
bot = telebot.TeleBot('YOUR_BOT_TOKEN')

# Command handler for '/start'
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,'Hi, I am Converter. My job is to convert various file formats into others. Additionally, I can help you download videos from different platforms using links.')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttonconvert = types.KeyboardButton("Convert File")
    buttondownload = types.KeyboardButton("Download Video")
    markup.row(buttonconvert, buttondownload)
    bot.send_message(message.chat.id, "Choose an Action", reply_markup=markup)

# Handler for the 'Download Video' button
@bot.message_handler(func=lambda message: message.text == "Download Video")
def buttons(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    youtube = types.KeyboardButton("YouTube")
    cansels = types.KeyboardButton("Menu")
    markup.row(youtube, cansels)
    bot.send_message(message.chat.id, "Select a Platform", reply_markup=markup)

# Handler for 'YouTube' button
@bot.message_handler(func=lambda message: message.text == "YouTube")
def youtubelinkdownload(message):
    bot.send_message(message.chat.id, "Please send the link to the YouTube video.")

# Handler for YouTube links
@bot.message_handler(func=lambda message: message.text.startswith(("https://www.youtube.com", "https://youtu.be")))
def handle_youtube_link(message):
    chat_id = message.chat.id
    youtube_link = message.text

    yt = YouTube(youtube_link)
    video = yt.streams.filter(progressive=True, file_extension='mp4').first()

    if video:
        video_path = video.download()
        with open(video_path, "rb") as video_file:
            bot.send_video(chat_id, video_file)

        os.remove(video_path)
    else:
        bot.send_message(chat_id, "Sorry, unable to download the video.")

# Handler for 'Convert File' button
@bot.message_handler(func=lambda message: message.text == "Convert File")
def handle_convert_button(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    format_button = types.KeyboardButton("Convert Mp4 to Mp3")
    markup.row(format_button)
    bot.send_message(message.chat.id, "Choose a format for conversion", reply_markup=markup)

# Handler for 'Convert Mp4 to Mp3' button
@bot.message_handler(func=lambda message: message.text == "Convert Mp4 to Mp3")
def handle_button_click(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    cancel = types.KeyboardButton("Menu")
    markup.row(cancel)
    bot.send_message(message.chat.id, "Send me the video", reply_markup=markup)

# Handler for incoming videos
@bot.message_handler(content_types=['video'])
def handle_video(message):
    chat_id = message.chat.id
    file_info = bot.get_file(message.video.file_id)
    file_path = file_info.file_path

    video_url = f"https://api.telegram.org/file/botYOUR_BOT_TOKEN/{file_path}"
    video_path = "input_video.mp4"
    os.system(f"wget '{video_url}' -O {video_path}")

    video_clip = VideoFileClip(video_path)
    audio_clip = video_clip.audio
    audio_path = "output_audio.mp3"
    audio_clip.write_audiofile(audio_path)

    with open(audio_path, "rb") as audio_file:
        bot.send_audio(chat_id, audio_file)

    os.remove(video_path)
    os.remove(audio_path)

# Handler for 'Menu' button@bot.message_handler(func=lambda message: message.text == "Menu")
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttonconvert = types.KeyboardButton("Convert File")
    buttondownload = types.KeyboardButton("Download Video")
    markup.row(buttonconvert, buttondownload)
    bot.send_message(message.chat.id, "Choose an Action", reply_markup=markup)

bot.polling()