import telebot
import config
import transfer
import os

config = config.Config("config.json")

bot = telebot.TeleBot(config.token)

content = {}


@bot.message_handler(content_types=['photo'])
def process_message(message):
    file_id = message.photo[-1].file_id
    if message.chat.id in content:
        content_file_info = bot.get_file(content.pop(message.chat.id))
        style_file_info = bot.get_file(file_id)

        content_file = bot.download_file(content_file_info.file_path)
        style_file = bot.download_file(style_file_info.file_path)

        with open("content.jpg", "wb") as content_image:
            content_image.write(content_file)

        with open("style.jpg", "wb") as style_image:
            style_image.write(style_file)

        transfer.transfer()
        os.remove("content.jpg")
        os.remove("style.jpg")
        with open("result.jpg", "rb") as result_image:
            bot.send_photo(message.chat.id, result_image)
        os.remove("result.jpg")
    else:
        content[message.chat.id] = file_id


if __name__ == "__main__":
    bot.polling(none_stop=True)
