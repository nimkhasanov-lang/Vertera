"""
Telegram Business Support Bot
O'zbek va Rus tillarini qo'llab-quvvatlaydi
Kerakli kutubxona: pip install pyTelegramBotAPI
"""

import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Token Railway Variables dan olinadi
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

# Foydalanuvchilarning tanlagan tili saqlanadi
user_lang = {}

# ==============================
# MATNLAR (O'zbek / Rus)
# ==============================
TEXTS = {
    "uz": {
        "welcome": (
            "👋 Salom! Xizmatimizga xush kelibsiz!\n\n"
            "Iltimos, tilni tanlang:"
        ),
        "lang_chosen": "✅ O'zbek tili tanlandi!",
        "ask_question": (
            "📩 Savolingiz yoki murojaatingizni yozing.\n\n"
            "Operatorlarimiz tez orada javob berishadi. 🕐"
        ),
        "received": (
            "✅ Murojaatingiz qabul qilindi!\n\n"
            "📋 *Sizning xabaringiz:*\n_{msg}_\n\n"
            "⏳ Operatorlarimiz 24 soat ichida javob berishadi.\n"
            "Boshqa savol bo'lsa, yozing! 😊"
        ),
        "help": "Savol yoki muammoingizni yozing, yordam beramiz! 💬",
    },
    "ru": {
        "welcome": (
            "👋 Здравствуйте! Добро пожаловать!\n\n"
            "Пожалуйста, выберите язык:"
        ),
        "lang_chosen": "✅ Выбран русский язык!",
        "ask_question": (
            "📩 Напишите ваш вопрос или обращение.\n\n"
            "Наши операторы скоро ответят вам. 🕐"
        ),
        "received": (
            "✅ Ваше обращение принято!\n\n"
            "📋 *Ваше сообщение:*\n_{msg}_\n\n"
            "⏳ Операторы ответят в течение 24 часов.\n"
            "Если есть другие вопросы — пишите! 😊"
        ),
        "help": "Напишите ваш вопрос или проблему, мы поможем! 💬",
    },
}

# ==============================
# TIL TANLASH TUGMALARI
# ==============================
def language_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data="lang_uz"),
        InlineKeyboardButton("🇷🇺 Русский",   callback_data="lang_ru"),
    )
    return markup

# ==============================
# /start KOMANDASI
# ==============================
@bot.message_handler(commands=["start"])
def start(message):
    chat_id = message.chat.id
    # Avvalgi til tanlovini tozalaymiz
    user_lang.pop(chat_id, None)
    bot.send_message(
        chat_id,
        TEXTS["uz"]["welcome"],   # Xush kelibsiz matni O'zbekcha
        reply_markup=language_keyboard(),
    )

# ==============================
# /help KOMANDASI
# ==============================
@bot.message_handler(commands=["help"])
def help_cmd(message):
    chat_id = message.chat.id
    lang = user_lang.get(chat_id, "uz")
    bot.send_message(chat_id, TEXTS[lang]["help"])

# ==============================
# TIL TANLASH (CALLBACK)
# ==============================
@bot.callback_query_handler(func=lambda call: call.data.startswith("lang_"))
def choose_language(call):
    chat_id = call.message.chat.id
    lang = call.data.split("_")[1]   # "uz" yoki "ru"
    user_lang[chat_id] = lang

    # Tugmani o'chirib, tasdiqlash xabari yuborish
    bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=None)
    bot.send_message(chat_id, TEXTS[lang]["lang_chosen"])
    bot.send_message(chat_id, TEXTS[lang]["ask_question"])

# ==============================
# FOYDALANUVCHI XABARI
# ==============================
@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    chat_id = message.chat.id

    # Agar til tanlanmagan bo'lsa — qayta tanlashni so'raymiz
    if chat_id not in user_lang:
        bot.send_message(
            chat_id,
            TEXTS["uz"]["welcome"],
            reply_markup=language_keyboard(),
        )
        return

    lang = user_lang[chat_id]
    user_text = message.text

    # Foydalanuvchiga tasdiqlash xabari
    reply = TEXTS[lang]["received"].format(msg=user_text)
    bot.send_message(chat_id, reply, parse_mode="Markdown")

    # ------------------------------------------------
    # ADMIN XABARINI YUBORISH (ixtiyoriy)
    # Adminning chat_id sini shu yerga qo'shing:
    # ADMIN_CHAT_ID = 123456789
    # bot.send_message(
    #     ADMIN_CHAT_ID,
    #     f"📨 Yangi murojaat!\n"
    #     f"👤 Foydalanuvchi: @{message.from_user.username} (ID: {chat_id})\n"
    #     f"🌐 Til: {lang.upper()}\n"
    #     f"💬 Xabar: {user_text}"
    # )
    # ------------------------------------------------

# ==============================
# BOTNI ISHGA TUSHIRISH
# ==============================
if __name__ == "__main__":
    print("✅ Bot ishga tushdi...")
    bot.infinity_polling()
