import os
import replicate
import requests
import telebot

TELEGRAM_BOT_TOKEN = "6990432139:AAEr7pCnxaptZ_mcrJQPompKtJivtTjpCWA"
REPLICATE_API_TOKEN = "r8_5b1hGbLvCLXl2dVzl4uNqShhApwgmeR3CaXLR"

# Set the REPLICATE_API_TOKEN environment variable
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

# инициализируем телебота
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(
        message, "Добрый день, пришлите нам фотографию\nи немного подождите..."
    )


@bot.message_handler(content_types=["photo"])
def handle_photo(message):
    # создаем фото
    file_id = message.photo[-1].file_id

    # инфо о файле
    file_info = bot.get_file(file_id)

    # качаем фото в локальную фс
    downloaded_file = bot.download_file(file_info.file_path)
    with open("received_image.jpg", "wb") as new_file:
        new_file.write(downloaded_file)

    # подключаем репликейт АПИ
    output = replicate.run(
        "microsoft/bringing-old-photos-back-to-life:c75db81db6cbd809d93cc3b7e7a088a351a3349c9fa02b6d393e35e0d51ba799",
        input={
            "HR": False,
            "image": open("received_image.jpg", "rb"),
            "with_scratch": True,
        },
    )

    # Отправляем готовое фото юзеру
    bot.send_photo(message.chat.id, output, caption="Ваш снимок готов")


if __name__ == "__main__":
    bot.polling()
