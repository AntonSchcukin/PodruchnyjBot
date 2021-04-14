import threading

import telebot, schedule, sqlite3, time, datetime
from multiprocessing import *
bot = telebot.TeleBot("1680703308:AAFYj5I9_ZpvVpSf2nZrTO3W3ovt49UyAIc")
papa_id = '1062973400'
channel_name = '-1001497838043'
post_time = '17:00'


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


class P_schedule():
    def start_schedule():
        schedule.every().tuesday.at(post_time).do(run_threaded, public_post)
        schedule.every().thursday.at(post_time).do(run_threaded, public_post)
        schedule.every().saturday.at(post_time).do(run_threaded, public_post)

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
       # bot.send_message(channel_name, post)
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
        cursor.execute("SELECT id, posts FROM datas")
        res = cursor.fetchall()
        bot.send_message(message.chat.id, '\n'.join([str(post[0]) + ". " + post[1] for post in res])
                         if len(res) > 0 else "В очереди нет постов.")
    elif message.text.split()[0] == '/delete':
        try:
            cursor.execute(f"DELETE FROM datas WHERE id={message.text.split()[1]}")
            db.commit()
            bot.send_message(message.chat.id, "Пост успешно удалён!")
        except:
            bot.send_message(message.chat.id, "Ошибка!")
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
