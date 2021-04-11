import telebot, schedule, sqlite3, time, datetime
from multiprocessing import *
bot = telebot.TeleBot("1680703308:AAFYj5I9_ZpvVpSf2nZrTO3W3ovt49UyAIc")
papa_id = '1062973400'
channel_name = '-1001497838043'
post_time = '17:00'


class P_schedule():
    def __init__(self):
        pass

    def start_schedule(self):
        schedule.every().tuesday.at(post_time).do(public_post)
        schedule.every().thursday.at(post_time).do(public_post)
        schedule.every().saturday.at(post_time).do(public_post)

        while True:
            schedule.run_pending()
            time.sleep(1)


def start_process():
    p1 = Process(target=P_schedule.start_schedule, args=()).start()


def public_post():
    try:
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        cursor.execute("SELECT posts FROM datas")
        post = cursor.fetchone()[0]
        bot.send_message(channel_name, post)
        bot.send_message(papa_id, f'Новый пост был опубликован. Постов в очереди: {len(cursor.fetchall())}')
        cursor.execute(f"DELETE FROM datas WHERE posts='{post}'")
        db.commit()
    except:
        bot.send_message(papa_id, f'Посты в очереди закончились. Ничего не опубликованно(')


@bot.message_handler(content_types='text')
def post(message):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    if message.text == '/order':
        cursor.execute("SELECT posts FROM datas")
        bot.send_message(message.chat.id, '\n'.join([post[0] for post in cursor.fetchall()]))
    else:
        cursor.execute("INSERT INTO datas(posts) VALUES(?)", (message.text,))
        db.commit()
        bot.send_message(message.chat.id, "Пост добавлен в очередь!")


if __name__ == '__main__':
    start_process()
    try:
        bot.polling(none_stop=True)
    except:
        pass