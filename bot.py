import telebot
from voice import get_mp3_file, get_file_name
from parser import get_article_text, get_article_language, get_link


@bot.message_handler(commands=['start'])
def forward_message(message):
    bot.send_message(message.from_user.id, "Привет, я перевожу статьи в аудиофайлы,"
                     "пришли мне ссылку на статью,"
                     "а я сброшу тебе mp3 файл.")

is_running = False

@bot.message_handler(content_types=['text'])
def forward_message(message):
    global is_running
    if not is_running:
        link = get_link(message.text)
        if link:
            is_running = True
            article_text = get_article_text(article_text)
            article_language = get_article_language(article_text)
            if article_language:
                bot.send_message(message.from_user.id, "Да эта статья нам подходит.")
                bot.send_message(message.from_user.id, f"Язык статьи - {article_language[0]}.")
                bot.send_message(message.from_user.id, "Отправляю аудиофайл...")
                file_name = get_file_name(link)
                get_mp3_file(file_name, article_text, article_language[1])
                bot.send_audio(message.from_user.id, audio=open(file_name, 'rb'))
            else:
                bot.send_message(message.from_user.id, "Данная статья не подходит,"
                                                        "попробуй другую...")
            is_running = False
        else:
            bot.send_message(message.from_user.id, "Нет, это не ссылка, попробуй "
                                                   "прислать ссылку на статью.")
    else:
        bot.send_message(message.from_user.id, "Я занят предыдущим запросом,"
                                                "подожди немного...")

