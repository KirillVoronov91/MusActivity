import logging
import random
import sys
import os

import telebot
from telebot import types
import time
from time import sleep
import threading
# Подключение к базе данных
import sqlite3
# При помощи билиотеки os создаем путь к файлу, который будет работать в любом репозитории
project_root_dir = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(os.path.join(project_root_dir, 'db', 'users_base'), check_same_thread=False)
cursor = conn.cursor()

# Импортируем созданные классы для получения данных из базы данных
from utils.database_classes import UserInfo

user_info = UserInfo(conn, cursor)

from utils.database_classes import team_mode_UserPointsChat

team_mode_user_pointsChat = team_mode_UserPointsChat(conn, cursor)

from utils.database_classes import self_mode_UserPointsChat

self_mode_user_pointsChat = self_mode_UserPointsChat(conn, cursor)

from utils.database_classes import Songs

random_song = Songs(cursor)

from utils.database_classes import update_tasks_and_songs

update_tasks_and_songs = update_tasks_and_songs(cursor)


# Функция, конвертирующая время в удобный формат
def timeconv(x):
    return time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(x))


# Создаем экземпляр бота
token = 'ТОКЕН, полученный при создании бота в BothFather'
bot = telebot.TeleBot(token)

# Список игровых заданий
self_mode_tasks = {
    'task1': '🌍 Перевести на иностранный язык',
    'task2': '🗣️ Объяснить своими словами',
    'task3': '🆚 Прочитать антонимами',
    'task4': '🎼 Пропеть мотив',
    'task5': '🎨 Нарисовать',
    'task6': '😀 Изобразить при помощи эмодзи',
    'task7': '❓ Отвечать на вопросы да/нет',
    'task8': '🐊 Показать',
    'task9': '⚠️ Объяснить словами на «С» и «П»:',
}

team_mode_tasks = {
    'task1': '🌍 Перевести на ин. язык (2 балла)',
    'task2': '🗣️ Объяснить своими словами (1 балл)',
    'task3': '🆚 Прочитать антонимами (1 балл)',
    'task4': '🎼 Пропеть мотив (1,5 балла)',
    'task5': '🎨 Нарисовать (2 балла)',
    'task6': '😀 Изобразить эмодзи (2 балла)',
    'task7': '❓ Отвечать на вопросы да/нет (1 балл)',
    'task8': '🐊 Показать (1,5 балла)',
    'task9': '⚠️ Объяснить словами на С и П: (1.5 б.)',
}
tasks_scores = {'⚠️ Объяснить словами на С и П: (1.5 б.)':1.5, '❓ Отвечать на вопросы да/нет (1 балл)': 1, '😀 Изобразить эмодзи (2 балла)':2, '🌍 Перевести на ин. язык (2 балла)': 2, '🗣️ Объяснить своими словами (1 балл)': 1,
                '🆚 Прочитать антонимами (1 балл)': 1, '🎼 Пропеть мотив (1,5 балла)': 1.5,
                '🎨 Нарисовать (2 балла)': 2, '🐊 Показать (1,5 балла)': 1.5}

# Для синхронизации потоков
lock = threading.Lock()
# Словарь, используемый для таймеров
team_mode_user_timers = {}
self_mode_user_timers = {}

# Переменная markup_choose_mode для перехода после нажатия кнопки "go"
from utils.buttons import Choose_mode_menu_keyboard

choose_mode_keyboard = Choose_mode_menu_keyboard()
markup_choose_mode = choose_mode_keyboard.keyboard

# Переменная markup_rules для перехода после нажатия кнопки "правила"
from utils.buttons import RulesKeyboard

rules_keyboard = RulesKeyboard()
markup_rules = rules_keyboard.keyboard

# Переменная markup_stat для перехода после нажатия кнопки "статистика"
from utils.buttons import StatKeyboard

stat_keyboard = StatKeyboard()
markup_stat = stat_keyboard.keyboard

from utils.buttons import AfterStatKeyboardModes

after_stat_keyboard_modes = AfterStatKeyboardModes()
markup_after_stat_modes = after_stat_keyboard_modes.keyboard

from utils.buttons import StatKeyboardModes

stat_keyboard_modes = StatKeyboardModes()
markup_stat_modes = stat_keyboard_modes.keyboard

# Переменные - кнопки, появляющиеся после выбора режима игры
from utils.buttons import Get_song_keyboard_self_mode

self_mode_get_task_keyboard = Get_song_keyboard_self_mode()
markup_get_song_self_mode = self_mode_get_task_keyboard.keyboard

from utils.buttons import Get_song_keyboard_team_mode

get_task_keyboard1 = Get_song_keyboard_team_mode()
markup_get_song_team_mode = get_task_keyboard1.keyboard

# Переменные - кнопки, появляющиеся после нажатия кнопки "выбрать жанр"
from utils.buttons import genres_team

genres_team_keyboard = genres_team()
markup_genres_team = genres_team_keyboard.keyboard

from utils.buttons import genres_self

genres_self_keyboard = genres_self()
markup_genres_self = genres_self_keyboard.keyboard

# Переменные - кнопки, появляющиеся после нажатия кнопки "выбрать временной период"
from utils.buttons import times_team

times_team_keyboard = times_team()
markup_times_team = times_team_keyboard.keyboard

from utils.buttons import times_self

times_self_keyboard = times_self()
markup_times_self = times_self_keyboard.keyboard

# Переменные - кнопки, появляющиеся после получения песни - выбор другой песни или получение задания
from utils.buttons import Chosen_song_keyboard_team_mode

chosen_song_keyboard_team_mode = Chosen_song_keyboard_team_mode()
markup_chosen_song_team_mode = chosen_song_keyboard_team_mode.keyboard

from utils.buttons import Chosen_song_keyboard_self_mode

chosen_song_keyboard_self_mode = Chosen_song_keyboard_self_mode()
markup_chosen_song_self_mode = chosen_song_keyboard_self_mode.keyboard

# Переменные - кнопки, появляющиеся после выбора песни и задания, перехода к таймеру
from utils.buttons import Timers_keyboard_self_mode

timers_keyboard_self_mode = Timers_keyboard_self_mode()
markup_timers_self_mode = timers_keyboard_self_mode.keyboard

from utils.buttons import Timers_keyboard_team_mode

timers_keyboard_team_mode = Timers_keyboard_team_mode()
markup_timers_team_mode = timers_keyboard_team_mode.keyboard

# Переменная markup_after_timers = кнопки, которые появляются после процесса объяснения песни,
# после кнопок с таймерами и "перейти далее"
from utils.buttons import After_timers_keyboard_team_mode

after_timers_keyboard_team_mode = After_timers_keyboard_team_mode()
markup_after_timers_team_mode = after_timers_keyboard_team_mode.keyboard

from utils.buttons import Self_mode_after_timers_keyboard

self_mode_after_timers_keyboard = Self_mode_after_timers_keyboard()
markup_self_mode_after_timers = self_mode_after_timers_keyboard.keyboard

# Переменная для прерывания таймера
from utils.buttons import Break_timer_keyboard_team_mode

breaktimer_keyboard_team_mode = Break_timer_keyboard_team_mode()
markup_breaktimer_team_mode = breaktimer_keyboard_team_mode.keyboard

from utils.buttons import self_mode_break_timer_keyboard

self_mode_breaktimer_keyboard = self_mode_break_timer_keyboard()
markup_self_mode_breaktimer = self_mode_breaktimer_keyboard.keyboard

# Переменная для окончания игры
from utils.buttons import Finish_keyboard_modes

finish_keyboard = Finish_keyboard_modes()
markup_finish = finish_keyboard.keyboard


# Функции для корректной работы таймеров
def start_timer60(user_id):
    team_mode_user_timers[user_id] = 60  # время таймера по умолчанию - 60 секунд
    msg_id = bot.send_message(user_id, 'Таймер запущен. Осталось 60 секунд').message_id
    for t in range(team_mode_user_timers[user_id], -1, -5):
        if team_mode_user_timers[user_id] == 0:
            break
        bot.edit_message_text(chat_id=user_id, message_id=msg_id, text=f'Осталось секунд: {t} ')
        sleep(5)
    bot.edit_message_text(chat_id=user_id, message_id=msg_id, text='Время вышло! Как ваши успехи?',
                          reply_markup=markup_after_timers_team_mode)


def self_mode_start_timer60(user_id):
    self_mode_user_timers[user_id] = 60  # время таймера по умолчанию - 60 секунд
    msg_id = bot.send_message(user_id, 'Таймер запущен. Осталось 60 секунд').message_id
    for t in range(self_mode_user_timers[user_id], -1, -5):
        if self_mode_user_timers[user_id] == 0:
            break
        bot.edit_message_text(chat_id=user_id, message_id=msg_id, text=f'Осталось секунд: {t} ')
        sleep(5)
    bot.edit_message_text(chat_id=user_id, message_id=msg_id,
                          text='Время вышло! Тот, кто отгадал песню должен нажать 👇',
                          reply_markup=markup_self_mode_after_timers)


# Обработка команды Старт
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    # Проверим, есть ли пользователь в таблице users_info
    cursor2 = conn.execute('SELECT user_id FROM users_info WHERE user_id = ?', (user_id,))
    row = cursor2.fetchone()
    if row is not None:
        us_id = message.from_user.id
        us_name = message.from_user.first_name
        us_sname = message.from_user.last_name
        username = message.from_user.username
        query = 'UPDATE users_info SET user_name = ?, user_surname = ?, username = ? WHERE user_id = ?'
        values = (us_name, us_sname, username, us_id)
        cursor.execute(query, values)
        conn.commit()
        # пользователь уже есть в базе данных
        bot.send_message(message.from_user.id, text="Привет, {0.first_name}! Добро пожаловать в МузАктивити!"
                                                    " \nНажмите команду /go чтобы начать игру".format(
            message.from_user))
    else:
        bot.send_message(message.from_user.id, text="Привет, {0.first_name}! Добро пожаловать в МузАктивити!"
                                                    " \nНажмите команду /go чтобы начать игру".format(
            message.from_user))
        us_id = message.from_user.id
        us_name = message.from_user.first_name
        us_sname = message.from_user.last_name
        username = message.from_user.username
        user_info.add_user(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username)


# Обработка команды go (Начать игру, продолжить игру)
@bot.message_handler(commands=['go'])
def go(message):
    bot.send_message(message.chat.id, text="Перед началом игры выберите один из режимов. "
                                           "Подробнее о каждом можно почитать в правилах 😀 ".format(message.from_user),
                     reply_markup=markup_choose_mode)
    # Проверим, есть ли чат в таблице chats_info
    chat_id = message.chat.id
    cht = message.chat.title
    cursor3 = conn.execute('SELECT chat_id FROM chats_info WHERE chat_id = ?', (chat_id,))
    row2 = cursor3.fetchone()
    if row2 is None:
        # если чата еще нет, добавляем его
        user_info.add_chat(chat_id=chat_id, chat_title=cht)


# Обработка команды Rules (правила)
@bot.message_handler(commands=['rules'])
def rules(message):
    bot.send_message(message.chat.id, '''
<b>Перед началом игры:</b>
- Соберите весёлую компанию (от 3 человек для игры в режиме "каждый сам за себя", от 4 для игры в командном режиме);
- Создайте групповой чат, добавив туда всех игроков и МузАктивити-бота
- Не будут лишними бумага и письменные принадлежности - в одном из заданий нужно рисовать, но это опционально - задание можно менять
- Каждый игрок должен инициировать чат с ботом, чтобы иметь возможность получать тексты песен. Для этого необходимо один раз совершить два действия:
- Нажать @Musactivity_bot 
- В открывшемся чате нажать кнопку Старт
В дальнейшем повторять эти действия нужно только если вы поменяли имя (фамилию, никнейм) в Телеграм и хотите, 
чтобы МузАктивити запомнил вас по новой.

<b>Суть игры:</b>
- В этом чате вы будете получать задания, с помощью которых вам будет необходимо объяснить текст песни, 
полученной от бота в личные сообщения. 
- Задания могут быть разными - от показывания песни жестами или напевания мотива 
до объяснения при помощи антонимов или рисунков.

<b>Режим "Каждый сам за себя":</b>
- В этом режиме один игрок объясняет полученную песню всем игрокам - балл зарабатывает тот, кто первым отгадал, какая песня была загадана. 
Этот же игрок объясняет песню следующим.
Вы можете договориться, что песню надо объяснить за 1 минуту (или другое время) или без учета времени.
Побеждает тот, кто по итогам игровой сессии получил больше всего очков. 

<b>Командный режим:</b>
- В этом режиме вам необходимо разбиться на команды и по очереди объяснять песни своим сокомандникам
- Получив песню, вы выбираете задание - в командном режиме у каждого задания есть своя стоимость.
- Также, предварительно договоритесь о времени на объяснение песни
- По окончанию времени, игрок, который объяснял песню должен нажать на кнопку с тем количеством баллов, которые его команда получает (в зависимости от стоимости задания)
- После этого ход переходит к другой команде
- Побеждает та команда, чьи игроки в сумме получили больше всего очков. 

<b>Статистика:</b>
- Для корректного сбора результатов необходимо:
<u>В режиме "каждый сам за себя"</u>: все игроки должны играть со своего телефона с инициированным заранее чатом с МузАктивити-ботом
<u>В командном режиме </u>: кнопки получения баллов могут нажимать как все игроки отгадывающей команды, так и только капитаны команд
- После завершения игры необходимо нажать команду /finish и выбрать режим, в котором вы играли. Тогда в следующий раз статистика будет собираться с нуля.
- В любой момент вы можете посмотреть статистику за всю историю чата.

<b>Все предложенные правила</b> являются только рекомендациями:
Вы можете придумывать свои правила и режимы, свои задания для объяснения песен.
Вы можете пользоваться своими таймерами.
Вы можете пользоваться для игры всего одним телефоном на всю компанию - статистика в таком случае будет считаться некорректно, но вы можете вести подсчёт самостоятельно.

Если у вас есть интересные идеи заданий, обязательно пишите в поддержку (@Musactivity) и мы возможно добавим  их для всех игроков
 ''', parse_mode='html', reply_markup=markup_rules)

@bot.message_handler(commands=['tasks'])
def tasks_explanation(message):
    bot.send_message(message.chat.id, '''
Описание игровых заданий и рекомендации по их использованию здесь:    
https://telegra.ph/Igrovye-zadaniya-Muzaktiviti-06-10
 ''', parse_mode='html', reply_markup=markup_rules)


# Обработка команды Stat (статистика)
@bot.message_handler(commands=['stat'])
def stats_command(message):
    bot.send_message(message.chat.id, text=f'''Выберите режим игры, статистику по которому вы хотите увидеть 👇
    ''', parse_mode='html', reply_markup=markup_stat_modes)

# Обработка команды Finish (закончить игру)
@bot.message_handler(commands=['finish'])
def finish_commands(message):
    bot.send_message(message.chat.id, text=f'''Спасибо за игру!
Какой режим игры вы хотите закончить? 👇
    ''', parse_mode='html', reply_markup=markup_finish)


# Обработка нажатия кнопок выбора режима игры
@bot.callback_query_handler(func=lambda callback: callback.data in ['self_mode', 'team_mode'])
def handle_modes(callback):
    if callback.data == 'self_mode':
        bot.send_message(callback.message.chat.id,
                         'Вы можете получить песню случайным образом или выбрать определенный жанр '
                         'или временной период (1990-е, 2000-е  и т.д.) ',
                         reply_markup=markup_get_song_self_mode)
    elif callback.data == 'team_mode':
        bot.send_message(callback.message.chat.id,
                         'Вы можете получить песню случайным образом или выбрать определенный жанр '
                         'или временной период (1990-е, 2000-е  и т.д.)',
                         reply_markup=markup_get_song_team_mode)


# Обработка нажатия кнопок получения песни в режиме "каждый сам за себя"
@bot.callback_query_handler(func=lambda callback: callback.data in ['self_mode_random_song',
                                                                    'self_mode_genre', 'self_mode_period'])
def handle_menu_self_mode(callback):
    if callback.data == 'self_mode_random_song':
        bot.answer_callback_query(callback.id)
        # Пользователь может начать игру из группового чата, не нажимая до этого кнопку start,
        # поэтому добавим еще одну проверку его на присутствие в users_info
        ch = callback.message.chat.id
        us_id = callback.from_user.id
        datetime = callback.message.date
        cursor2 = conn.execute('SELECT user_id FROM users_info WHERE user_id = ?', (us_id,))
        row = cursor2.fetchone()
        if row is not None:
            # пользователь уже есть в базе данных
            bot.send_message(callback.message.chat.id, f'''
Текст загаданной песни отправился в ваш личный чат с МузАктивити ботом.
Если его нет, то надо создать😉
Чтобы получить задание или поменять песню жмите здесь 👇''', parse_mode='html',
                             reply_markup=markup_chosen_song_self_mode)
        else:
            us_id = callback.from_user.id
            us_name = callback.from_user.first_name
            us_sname = callback.from_user.last_name
            username = callback.from_user.username
            user_info.add_user(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username)
            bot.send_message(callback.message.chat.id, f'''
Текст загаданной песни отправился в ваш личный чат с МузАктивити ботом.
Если его нет, то надо создать😉
Чтобы получить задание или поменять песню жмите здесь 👇''',
                             parse_mode='html', reply_markup=markup_chosen_song_self_mode)
        # Получаем случайную песню
        song_id, formatted_song = random_song.get_random_song()  # распаковка кортежа
        #  добавляем данные в таблицу user_tasks
        query = "INSERT INTO user_songs (chat_id, user_id, start_session, song_id, is_skip) VALUES (?, ?, ?, ?, ?)"
        values = (ch, us_id, timeconv(datetime), song_id, 0)
        cursor.execute(query, values)
        conn.commit()
        bot.send_message(callback.from_user.id, f'{formatted_song}', parse_mode='html')
    elif callback.data == 'self_mode_genre':
        bot.answer_callback_query(callback.id)
        bot.send_message(callback.message.chat.id, 'Выберите жанр, песню из которого вы хотите объяснить',
                         reply_markup=markup_genres_self)
    elif callback.data == 'self_mode_period':
        bot.answer_callback_query(callback.id)
        bot.send_message(callback.message.chat.id, 'Выберите временной период, песню из которого вы хотите объяснить',
                         reply_markup=markup_times_self)


# Обработка нажатия кнопок получения песни в режиме "командный"
@bot.callback_query_handler(
    func=lambda callback: callback.data in ['team_mode_random_song', 'team_mode_genre', 'team_mode_period'])
def handle_menu_team_mode(callback):
    if callback.data == 'team_mode_random_song':
        bot.answer_callback_query(callback.id)
        # Та же проверка, что и в режиме "сам за себя"
        ch = callback.message.chat.id
        us_id = callback.from_user.id
        datetime = callback.message.date
        cursor2 = conn.execute('SELECT user_id FROM users_info WHERE user_id = ?', (us_id,))
        row = cursor2.fetchone()
        if row is not None:
            # пользователь уже есть в базе данных
            bot.send_message(callback.message.chat.id, f'''
Текст загаданной песни отправился в ваш личный чат с МузАктивити ботом.
Если его нет, то надо создать😉
Чтобы получить задание или поменять песню жмите здесь 👇''',
                             parse_mode='html', reply_markup=markup_chosen_song_team_mode)
        else:
            us_id = callback.from_user.id
            us_name = callback.from_user.first_name
            us_sname = callback.from_user.last_name
            username = callback.from_user.username
            user_info.add_user(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username)
            bot.send_message(callback.message.chat.id, f'''
Текст загаданной песни отправился в ваш личный чат с МузАктивити ботом.
Если его нет, то надо создать😉
Чтобы получить задание или поменять песню жмите здесь 👇''',
                             parse_mode='html', reply_markup=markup_chosen_song_team_mode)
        # Получаем случайную песню
        song_id, formatted_song = random_song.get_random_song()  # распаковка кортежа
        #  добавляем данные в таблицу user_tasks
        query = "INSERT INTO user_songs (chat_id, user_id, start_session, song_id, is_skip) VALUES (?, ?, ?, ?, ?)"
        values = (ch, us_id, timeconv(datetime), song_id, 0)
        cursor.execute(query, values)
        conn.commit()
        bot.send_message(callback.from_user.id, f'{formatted_song}', parse_mode='html')
    elif callback.data == 'team_mode_genre':
        bot.answer_callback_query(callback.id)
        bot.send_message(callback.message.chat.id, 'Выберите жанр, песню из которого вы хотите объяснить',
                         reply_markup=markup_genres_team)
    elif callback.data == 'team_mode_period':
        bot.answer_callback_query(callback.id)
        bot.send_message(callback.message.chat.id, 'Выберите временной период, песню из которого вы хотите объяснить',
                         reply_markup=markup_times_team)


# Обработка нажатия кнопок получения жанра в режиме "командный"
@bot.callback_query_handler(func=lambda callback: callback.data in ['rock_song_team', 'pop_song_team', 'bard_song_team',
                                                                    'rap_song_team', 'movies_song_team'])
def handle_genres_team_mode(callback):
    if callback.data == 'rock_song_team':
        bot.answer_callback_query(callback.id)
        ch = callback.message.chat.id
        us_id = callback.from_user.id
        datetime = callback.message.date
        # Для статистики здесь и далее мы будем добавлять в таблицы genres и times данные о том,
        # какие жанры и временные периоды предпочитают выбирать пользователи
        genre = 'Рок'
        random_song.insert_genre_to_db(ch, us_id, timeconv(datetime), genre)
        bot.send_message(callback.message.chat.id, f'''
Текст загаданной песни отправился в ваш личный чат с МузАктивити ботом.
Если его нет, то надо создать😉
Чтобы получить задание или поменять песню жмите здесь 👇''',
                         parse_mode='html', reply_markup=markup_chosen_song_team_mode)
        rsong = random_song.get_song_rock(chat_id=ch, user_id=us_id, start_session=timeconv(datetime))
        bot.send_message(callback.from_user.id,
                         f'{rsong}',
                         parse_mode='html')
    elif callback.data == 'pop_song_team':
        bot.answer_callback_query(callback.id)
        ch = callback.message.chat.id
        us_id = callback.from_user.id
        datetime = callback.message.date
        genre = 'Поп'
        random_song.insert_genre_to_db(ch, us_id, timeconv(datetime), genre)
        bot.send_message(callback.message.chat.id, f'''
Текст загаданной песни отправился в ваш личный чат с МузАктивити ботом.
Если его нет, то надо создать😉
Чтобы получить задание или поменять песню жмите здесь 👇''',
                         parse_mode='html', reply_markup=markup_chosen_song_team_mode)
        rsong = random_song.get_song_pop(chat_id=ch, user_id=us_id, start_session=timeconv(datetime))
        bot.send_message(callback.from_user.id,
                         f'{rsong}',
                         parse_mode='html')
    elif callback.data == 'bard_song_team':
        bot.answer_callback_query(callback.id)
        ch = callback.message.chat.id
        us_id = callback.from_user.id
        datetime = callback.message.date
        genre = 'Барды, эстрада'
        random_song.insert_genre_to_db(ch, us_id, timeconv(datetime), genre)
        bot.send_message(callback.message.chat.id, f'''
Текст загаданной песни отправился в ваш личный чат с МузАктивити ботом.
Если его нет, то надо создать😉
Чтобы получить задание или поменять песню жмите здесь 👇''',
                         parse_mode='html', reply_markup=markup_chosen_song_team_mode)
        rsong = random_song.get_song_bards(chat_id=ch, user_id=us_id, start_session=timeconv(datetime))
        bot.send_message(callback.from_user.id,
                         f'{rsong}',
                         parse_mode='html')
    elif callback.data == 'rap_song_team':
        bot.answer_callback_query(callback.id)
        ch = callback.message.chat.id
        us_id = callback.from_user.id
        datetime = callback.message.date
        genre = 'Хип-хоп, Rnb, Рэп'
        random_song.insert_genre_to_db(ch, us_id, timeconv(datetime), genre)
        bot.send_message(callback.message.chat.id, f'''
Текст загаданной песни отправился в ваш личный чат с МузАктивити ботом.
Если его нет, то надо создать😉
Чтобы получить задание или поменять песню жмите здесь 👇''',
                         parse_mode='html', reply_markup=markup_chosen_song_team_mode)
        rsong = random_song.get_song_hip(chat_id=ch, user_id=us_id, start_session=timeconv(datetime))
        bot.send_message(callback.from_user.id,
                         f'{rsong}',
                         parse_mode='html')
    elif callback.data == 'movies_song_team':
        bot.answer_callback_query(callback.id)
        ch = callback.message.chat.id
        us_id = callback.from_user.id
        datetime = callback.message.date
        genre = 'Из фильмов и мультфильмов'
        random_song.insert_genre_to_db(ch, us_id, timeconv(datetime), genre)
        bot.send_message(callback.message.chat.id, f'''
Текст загаданной песни отправился в ваш личный чат с МузАктивити ботом.
Если его нет, то надо создать😉
Чтобы получить задание или поменять песню жмите здесь 👇''',
                         parse_mode='html', reply_markup=markup_chosen_song_team_mode)
        rsong = random_song.get_song_movies(chat_id=ch, user_id=us_id, start_session=timeconv(datetime))
        bot.send_message(callback.from_user.id,
                         f'{rsong}',
                         parse_mode='html')


# Обработка нажатия кнопок получения жанра в режиме "каждый сам за себя"
@bot.callback_query_handler(func=lambda callback: callback.data in ['rock_song_self', 'pop_song_self', 'bard_song_self',
                                                                    'rap_song_self', 'movies_song_self'])
def handle_genres_self_mode(callback):
    if callback.data == 'rock_song_self':
        bot.answer_callback_query(callback.id)
        ch = callback.message.chat.id
        us_id = callback.from_user.id
        datetime = callback.message.date
        genre = 'Рок'
        random_song.insert_genre_to_db(ch, us_id, timeconv(datetime), genre)
        bot.send_message(callback.message.chat.id, f'''
Текст загаданной песни отправился в ваш личный чат с МузАктивити ботом.
Если его нет, то надо создать😉
Чтобы получить задание или поменять песню жмите здесь 👇''',
                         parse_mode='html', reply_markup=markup_chosen_song_self_mode)
        rsong = random_song.get_song_rock(chat_id=ch, user_id=us_id, start_session=timeconv(datetime))
        bot.send_message(callback.from_user.id,
                         f'{rsong}',
                         parse_mode='html')
    elif callback.data == 'pop_song_self':
        bot.answer_callback_query(callback.id)
        ch = callback.message.chat.id
        us_id = callback.from_user.id
        datetime = callback.message.date
        genre = 'Поп'
        random_song.insert_genre_to_db(ch, us_id, timeconv(datetime), genre)
        bot.send_message(callback.message.chat.id, f'''
Текст загаданной песни отправился в ваш личный чат с МузАктивити ботом.
Если его нет, то надо создать😉
Чтобы получить задание или поменять песню жмите здесь 👇''',
                         parse_mode='html', reply_markup=markup_chosen_song_self_mode)
        rsong = random_song.get_song_pop(chat_id=ch, user_id=us_id, start_session=timeconv(datetime))
        bot.send_message(callback.from_user.id,
                         f'{rsong}',
                         parse_mode='html')
    elif callback.data == 'bard_song_self':
        bot.answer_callback_query(callback.id)
        ch = callback.message.chat.id
        us_id = callback.from_user.id
        datetime = callback.message.date
        genre = 'Барды, эстрада'
        random_song.insert_genre_to_db(ch, us_id, timeconv(datetime), genre)
        bot.send_message(callback.message.chat.id, f'''
Текст загаданной песни отправился в ваш личный чат с МузАктивити ботом.
Если его нет, то надо создать😉
Чтобы получить задание или поменять песню жмите здесь 👇''',
                         parse_mode='html', reply_markup=markup_chosen_song_self_mode)
        rsong = random_song.get_song_bards(chat_id=ch, user_id=us_id, start_session=timeconv(datetime))
        bot.send_message(callback.from_user.id,
                         f'{rsong}',
                         parse_mode='html')
    elif callback.data == 'rap_song_self':
        bot.answer_callback_query(callback.id)
        ch = callback.message.chat.id
        us_id = callback.from_user.id
        datetime = callback.message.date
        genre = 'Хип-хоп, Rnb, Рэп'
        random_song.insert_genre_to_db(ch, us_id, timeconv(datetime), genre)
        bot.send_message(callback.message.chat.id, f'''
Текст загаданной песни отправился в ваш личный чат с МузАктивити ботом.
Если его нет, то надо создать😉
Чтобы получить задание или поменять песню жмите здесь 👇''',
                         parse_mode='html', reply_markup=markup_chosen_song_self_mode)
        rsong = random_song.get_song_hip(chat_id=ch, user_id=us_id, start_session=timeconv(datetime))
        bot.send_message(callback.from_user.id,
                         f'{rsong}',
                         parse_mode='html')
    elif callback.data == 'movies_song_self':
        bot.answer_callback_query(callback.id)
        ch = callback.message.chat.id
        us_id = callback.from_user.id
        datetime = callback.message.date
        genre = 'Из фильмов и мультфильмов'
        random_song.insert_genre_to_db(ch, us_id, timeconv(datetime), genre)
        bot.send_message(callback.message.chat.id, f'''
Текст загаданной песни отправился в ваш личный чат с МузАктивити ботом.
Если его нет, то надо создать😉
Чтобы получить задание или поменять песню жмите здесь 👇''',
                         parse_mode='html', reply_markup=markup_chosen_song_self_mode)
        rsong = random_song.get_song_movies(chat_id=ch, user_id=us_id, start_session=timeconv(datetime))
        bot.send_message(callback.from_user.id,
                         f'{rsong}',
                         parse_mode='html')


# Обработка нажатия кнопок получения временного периода в режиме "командный"
@bot.callback_query_handler(
    func=lambda callback: callback.data in ['2020_song_team', '2010_song_team', '2000_song_team',
                                            '1990_song_team', 'ussr_song_team'])
def handle_times_team_mode(callback):
    if callback.data == '2020_song_team':
        bot.answer_callback_query(callback.id)
        ch = callback.message.chat.id
        us_id = callback.from_user.id
        datetime = callback.message.date
        times = '2020-е'
        random_song.insert_times_to_db(ch, us_id, timeconv(datetime), times)
        bot.send_message(callback.message.chat.id, f'''
Текст загаданной песни отправился в ваш личный чат с МузАктивити ботом.
Если его нет, то надо создать😉
Чтобы получить задание или поменять песню жмите здесь 👇''',
                         parse_mode='html', reply_markup=markup_chosen_song_team_mode)
        rsong = random_song.get_song_20(chat_id=ch, user_id=us_id, start_session=timeconv(datetime))
        bot.send_message(callback.from_user.id,
                         f'{rsong}',
                         parse_mode='html')
    elif callback.data == '2010_song_team':
        bot.answer_callback_query(callback.id)
        ch = callback.message.chat.id
        us_id = callback.from_user.id
        datetime = callback.message.date
        times = '2010-е'
        random_song.insert_times_to_db(ch, us_id, timeconv(datetime), times)
        bot.send_message(callback.message.chat.id, f'''
Текст загаданной песни отправился в ваш личный чат с МузАктивити ботом.
Если его нет, то надо создать😉
Чтобы получить задание или поменять песню жмите здесь 👇''',
                         parse_mode='html', reply_markup=markup_chosen_song_team_mode)
        rsong = random_song.get_song_10(chat_id=ch, user_id=us_id, start_session=timeconv(datetime))
        bot.send_message(callback.from_user.id,
                         f'{rsong}',
                         parse_mode='html')
    elif callback.data == '2000_song_team':
        bot.answer_callback_query(callback.id)
        ch = callback.message.chat.id
        us_id = callback.from_user.id
        datetime = callback.message.date
        times = '2000-е'
        random_song.insert_times_to_db(ch, us_id, timeconv(datetime), times)
        bot.send_message(callback.message.chat.id, f'''
Текст загаданной песни отправился в ваш личный чат с МузАктивити ботом.
Если его нет, то надо создать😉
Чтобы получить задание или поменять песню жмите здесь 👇''',
                         parse_mode='html', reply_markup=markup_chosen_song_team_mode)
        rsong = random_song.get_song_00(chat_id=ch, user_id=us_id, start_session=timeconv(datetime))
        bot.send_message(callback.from_user.id,
                         f'{rsong}',
                         parse_mode='html')
    elif callback.data == '1990_song_team':
        bot.answer_callback_query(callback.id)
        ch = callback.message.chat.id
        us_id = callback.from_user.id
        datetime = callback.message.date
        times = '1990-е'
        random_song.insert_times_to_db(ch, us_id, timeconv(datetime), times)
        bot.send_message(callback.message.chat.id, f'''
Текст загаданной песни отправился в ваш личный чат с МузАктивити ботом.
Если его нет, то надо создать😉
Чтобы получить задание или поменять песню жмите здесь 👇''',
                         parse_mode='html', reply_markup=markup_chosen_song_team_mode)
        rsong = random_song.get_song_90(chat_id=ch, user_id=us_id, start_session=timeconv(datetime))
        bot.send_message(callback.from_user.id,
                         f'{rsong}',
                         parse_mode='html')
    elif callback.data == 'ussr_song_team':
        bot.answer_callback_query(callback.id)
        ch = callback.message.chat.id
        us_id = callback.from_user.id
        datetime = callback.message.date
        times = 'Советский Союз'
        random_song.insert_times_to_db(ch, us_id, timeconv(datetime), times)
        bot.send_message(callback.message.chat.id, f'''
Текст загаданной песни отправился в ваш личный чат с МузАктивити ботом.
Если его нет, то надо создать😉
Чтобы получить задание или поменять песню жмите здесь 👇''',
                         parse_mode='html', reply_markup=markup_chosen_song_team_mode)
        rsong = random_song.get_song_ussr(chat_id=ch, user_id=us_id, start_session=timeconv(datetime))
        bot.send_message(callback.from_user.id,
                         f'{rsong}',
                         parse_mode='html')


# Обработка нажатия кнопок получения временного периода в режиме "каждый сам за себя"
@bot.callback_query_handler(
    func=lambda callback: callback.data in ['2020_song_self', '2010_song_self', '2000_song_self',
                                            '1990_song_self', 'ussr_song_self'])
def handle_times_self_mode(callback):
    if callback.data == '2020_song_self':
        bot.answer_callback_query(callback.id)
        ch = callback.message.chat.id
        us_id = callback.from_user.id
        datetime = callback.message.date
        times = '2020-е'
        random_song.insert_times_to_db(ch, us_id, timeconv(datetime), times)
        bot.send_message(callback.message.chat.id, f'''
Текст загаданной песни отправился в ваш личный чат с МузАктивити ботом.
Если его нет, то надо создать😉
Чтобы получить задание или поменять песню жмите здесь 👇''',
                         parse_mode='html', reply_markup=markup_chosen_song_self_mode)
        rsong = random_song.get_song_20(chat_id=ch, user_id=us_id, start_session=timeconv(datetime))
        bot.send_message(callback.from_user.id,
                         f'{rsong}',
                         parse_mode='html')
    elif callback.data == '2010_song_self':
        bot.answer_callback_query(callback.id)
        ch = callback.message.chat.id
        us_id = callback.from_user.id
        datetime = callback.message.date
        times = '2010-е'
        random_song.insert_times_to_db(ch, us_id, timeconv(datetime), times)
        bot.send_message(callback.message.chat.id, f'''
Текст загаданной песни отправился в ваш личный чат с МузАктивити ботом.
Если его нет, то надо создать😉
Чтобы получить задание или поменять песню жмите здесь 👇''',
                         parse_mode='html', reply_markup=markup_chosen_song_self_mode)
        rsong = random_song.get_song_10(chat_id=ch, user_id=us_id, start_session=timeconv(datetime))
        bot.send_message(callback.from_user.id,
                         f'{rsong}',
                         parse_mode='html')
    elif callback.data == '2000_song_self':
        bot.answer_callback_query(callback.id)
        ch = callback.message.chat.id
        us_id = callback.from_user.id
        datetime = callback.message.date
        times = '2000-е'
        random_song.insert_times_to_db(ch, us_id, timeconv(datetime), times)
        bot.send_message(callback.message.chat.id, f'''
Текст загаданной песни отправился в ваш личный чат с МузАктивити ботом.
Если его нет, то надо создать😉
Чтобы получить задание или поменять песню жмите здесь 👇''',
                         parse_mode='html', reply_markup=markup_chosen_song_self_mode)
        rsong = random_song.get_song_00(chat_id=ch, user_id=us_id, start_session=timeconv(datetime))
        bot.send_message(callback.from_user.id,
                         f'{rsong}',
                         parse_mode='html')
    elif callback.data == '1990_song_self':
        bot.answer_callback_query(callback.id)
        ch = callback.message.chat.id
        us_id = callback.from_user.id
        datetime = callback.message.date
        times = '1990-е'
        random_song.insert_times_to_db(ch, us_id, timeconv(datetime), times)
        bot.send_message(callback.message.chat.id, f'''
Текст загаданной песни отправился в ваш личный чат с МузАктивити ботом.
Если его нет, то надо создать😉
Чтобы получить задание или поменять песню жмите здесь 👇''',
                         parse_mode='html', reply_markup=markup_chosen_song_self_mode)
        rsong = random_song.get_song_90(chat_id=ch, user_id=us_id, start_session=timeconv(datetime))
        bot.send_message(callback.from_user.id,
                         f'{rsong}',
                         parse_mode='html')
    elif callback.data == 'ussr_song_self':
        bot.answer_callback_query(callback.id)
        ch = callback.message.chat.id
        us_id = callback.from_user.id
        datetime = callback.message.date
        times = 'Советский Союз'
        random_song.insert_times_to_db(ch, us_id, timeconv(datetime), times)
        bot.send_message(callback.message.chat.id, f'''
Текст загаданной песни отправился в ваш личный чат с МузАктивити ботом.
Если его нет, то надо создать😉
Чтобы получить задание или поменять песню жмите здесь 👇''',
                         parse_mode='html', reply_markup=markup_chosen_song_self_mode)
        rsong = random_song.get_song_ussr(chat_id=ch, user_id=us_id, start_session=timeconv(datetime))
        bot.send_message(callback.from_user.id,
                         f'{rsong}',
                         parse_mode='html')


# Обработка нажатия кнопок получения баллов за ответ в режиме "командный"
@bot.callback_query_handler(func=lambda callback: callback.data in ['right_answer_2', 'right_answer_15',
                                                                    'right_answer_1', 'wrong_answer'])
def inline_points_team_mode(callback):
    # Словарь с количеством баллов за каждый случай
    points_dict = {
        'right_answer_2': 2,
        'right_answer_15': 1.5,
        'right_answer_1': 1,
        'wrong_answer': 0
    }
    if callback.data in points_dict:
        bot.answer_callback_query(callback.id)
        us_id = callback.from_user.id
        ch = callback.message.chat.id
        datetime = callback.message.date
        points = points_dict.get(callback.data, 0)
        user = callback.from_user.first_name
        # добавляем данные в таблицу с очками в командном режиме - она используется для получения статистики по игре
        team_mode_user_pointsChat.add_points_chat(user_id=us_id, chat_id=ch, points=points, attempts=1,
                                                  right_answers=int(points > 0), false_answers=int(points == 0),
                                                  start_date=timeconv(datetime), game_status=1)
        if points > 1:
            bot.send_message(callback.message.chat.id,
                             f'Супер! {user}, ваша команда получает {points} балла! Ход переходит к следующей команде 👇',
                             reply_markup=markup_get_song_team_mode)
            # Обновляем данные в таблице user_songs
            query = 'UPDATE user_songs SET points = ? WHERE chat_id = ? AND is_skip = ? ' \
                    'AND id = (SELECT MAX(id) FROM user_songs WHERE chat_id = ?)'
            values = (points, ch, 0, ch)
            cursor.execute(query, values)
            conn.commit()
        elif points == 1:
            bot.send_message(callback.message.chat.id,
                             f'Супер! {user}, ваша команда получает {points} балл! Ход переходит к следующей команде 👇',
                             reply_markup=markup_get_song_team_mode)
            # Обновляем данные в таблице user_songs
            query = 'UPDATE user_songs SET points = ? WHERE chat_id = ? AND is_skip = ? ' \
                    'AND id = (SELECT MAX(id) FROM user_songs WHERE chat_id = ?)'
            values = (points, ch, 0, ch)
            cursor.execute(query, values)
            conn.commit()
        else:
            bot.send_message(callback.message.chat.id,
                             f'{user}, не расстраивайтесь! Это было непросто! Ход переходит к следующей команде 👇',
                             reply_markup=markup_get_song_team_mode)
            # Обновляем данные в таблице user_songs
            query = 'UPDATE user_songs SET points = ? WHERE chat_id = ? AND is_skip = ? ' \
                    'AND id = (SELECT MAX(id) FROM user_songs WHERE chat_id = ?)'
            values = (points, ch, 0, ch)
            cursor.execute(query, values)
            conn.commit()


# Обработчик нажатия клавиатуры, появившейся после нажатия кнопки "получить задание"
@bot.callback_query_handler(func=lambda callback: callback.data.startswith('task:'))
def handle_task(callback):
    task_key = callback.data.split(':', 1)[1]
    task_text = team_mode_tasks.get(task_key)
    task_score = tasks_scores.get(task_text)
    if task_text and task_score == 1:
        response_text = f'<b>Ваше задание</b>: {task_text}\n\nВыберите действие:'
        bot.send_message(callback.message.chat.id, response_text, parse_mode='html',
                         reply_markup=markup_timers_team_mode)
    elif task_text and task_score == 1.5:
        response_text = f'<b>Ваше задание</b>: {task_text}\n\nВыберите действие:'
        bot.send_message(callback.message.chat.id, response_text, parse_mode='html',
                         reply_markup=markup_timers_team_mode)
    elif task_text and task_score == 2:
        response_text = f'<b>Ваше задание</b>: {task_text}\n\nВыберите действие:'
        bot.send_message(callback.message.chat.id, response_text, parse_mode='html',
                         reply_markup=markup_timers_team_mode)
    else:
        bot.answer_callback_query(callback_query_id=callback.id, text='Ошибка: задание не найдено')


# Обработчик нажатия кнопок "правила, начать игру, продолжить игру, статистика, закончить игру"
@bot.callback_query_handler(
    func=lambda callback: callback.data in ['rules', 'start_game', 'continue', 'stat', 'finish'])
def inline_buttons(callback):
    if callback.data == 'rules':
        bot.send_message(callback.message.chat.id, '''
        <b>Перед началом игры:</b>
- Соберите весёлую компанию (от 3 человек для игры в режиме "каждый сам за себя", от 4 для игры в командном режиме);
- Создайте групповой чат, добавив туда всех игроков и МузАктивити-бота
- Не будут лишними бумага и письменные принадлежности - в одном из заданий нужно рисовать, но это опционально - задание можно менять
- Каждый игрок должен инициировать чат с ботом, чтобы иметь возможность получать тексты песен. Для этого необходимо один раз совершить два действия:
- Нажать @Musactivity_bot 
- В открывшемся чате нажать кнопку Старт
В дальнейшем повторять эти действия нужно только если вы поменяли имя (фамилию, никнейм) в Телеграм и хотите, 
чтобы МузАктивити запомнил вас по новой.

<b>Суть игры:</b>
- В этом чате вы будете получать задания, с помощью которых вам будет необходимо объяснить текст песни, 
полученной от бота в личные сообщения. 
- Задания могут быть разными - от показывания песни жестами или напевания мотива 
до объяснения при помощи антонимов или рисунков.


<b>Режим "Каждый сам за себя":</b>
- В этом режиме один игрок объясняет полученную песню всем игрокам - балл зарабатывает тот, кто первым отгадал, какая песня была загадана. 
Этот же игрок объясняет песню следующим.
Вы можете договориться, что песню надо объяснить за 1 минуту (или другое время) или без учета времени.
Побеждает тот, кто по итогам игровой сессии получил больше всего очков. 

<b>Командный режим:</b>
- В этом режиме вам необходимо разбиться на команды и по очереди объяснять песни своим сокомандникам
- Получив песню, вы выбираете задание - в командном режиме у каждого задания есть своя стоимость.
- Также, предварительно договоритесь о времени на объяснение песни
- По окончанию времени, игрок, который объяснял песню должен нажать на кнопку с тем количеством баллов, которые его команда получает (в зависимости от стоимости задания)
- После этого ход переходит к другой команде
- Побеждает та команда, чьи игроки в сумме получили больше всего очков. 

<b>Статистика:</b>
- Для корректного сбора результатов необходимо:
<u>В режиме "каждый сам за себя"</u>: все игроки должны играть со своего телефона с инициированным заранее чатом с МузАктивити-ботом
<u>В командном режиме </u>: кнопки получения баллов могут нажимать как все игроки отгадывающей команды, так и только капитаны команд
- После завершения игры необходимо нажать команду /finish и выбрать режим, в котором вы играли. Тогда в следующий раз статистика будет собираться с нуля.
- В любой момент вы можете посмотреть статистику за всю историю чата.

<b>Все предложенные правила</b> являются только рекомендациями:
Вы можете придумывать свои правила и режимы, свои задания для объяснения песен.
Вы можете пользоваться своими таймерами.
Вы можете пользоваться для игры всего одним телефоном на всю компанию - статистика в таком случае будет считаться некорректно, но вы можете вести подсчёт самостоятельно.

Если у вас есть интересные идеи заданий, обязательно пишите в поддержку (@Musactivity) и мы возможно добавим  их для всех игроков ''',
                         parse_mode='html', reply_markup=markup_rules)
    elif callback.data == 'start_game' and lock:
        bot.send_message(callback.message.chat.id,
                         'Перед началом игры выберите один из режимов. Подробнее о каждом можно почитать в правилах 😀',
                         reply_markup=markup_choose_mode)
    elif callback.data == 'continue' and lock:
        bot.send_message(callback.message.chat.id,
                         'Напомните, в каком режиме играем?',
                         reply_markup=markup_choose_mode)
    elif callback.data == 'stat' and lock:
        bot.send_message(callback.message.chat.id, text=f'''Выберите режим игры, статистику по которому вы хотите увидеть 👇
   
        ''', parse_mode='html', reply_markup=markup_stat_modes)
    elif callback.data == 'finish' and lock:
        bot.send_message(callback.message.chat.id, text=f'''Спасибо за игру!
Какой режим игры вы хотите закончить? 👇
        ''', parse_mode='html', reply_markup=markup_finish)


# Обработчик нажатия кнопки выбора режима игры для получения статистики
@bot.callback_query_handler(func=lambda callback: callback.data in ['stat_self_mode', 'stat_team_mode'])
def inline_stat_modes(callback):
    if callback.data == 'stat_self_mode' and lock:
        ch = callback.message.chat.id
        bot.send_message(callback.message.chat.id, text=f'''<u>Общая статистика чата:</u>
<b>Количество отгаданных песен:</b> {self_mode_user_pointsChat.self_mode_get_points_chat(chat_id=ch)}

<u>Текущая сессия:</u>
<b>Количество отгаданных песен:</b> {self_mode_user_pointsChat.self_mode_get_current_points_chat(chat_id=ch)}''',
                         parse_mode='html', reply_markup=markup_after_stat_modes)
    elif callback.data == 'stat_team_mode' and lock:
        ch = callback.message.chat.id
        bot.send_message(callback.message.chat.id, text=f'''<u>Общая статистика чата:</u>
<b>Количество попыток:</b> {team_mode_user_pointsChat.get_attempts_chat(chat_id=ch)}  
<b>Количество правильных ответов:</b> {team_mode_user_pointsChat.get_right_answers_chat(chat_id=ch)}  
<b>Количество очков:</b> {team_mode_user_pointsChat.get_points_chat(chat_id=ch)}

<u>Текущая сессия:</u>
<b>Количество попыток:</b> {team_mode_user_pointsChat.get_current_attempts_chat(chat_id=ch)}  
<b>Количество правильных ответов:</b> {team_mode_user_pointsChat.get_current_right_answers_chat(chat_id=ch)}  
<b>Количество очков:</b> {team_mode_user_pointsChat.get_current_points_chat(chat_id=ch)}
        ''', parse_mode='html', reply_markup=markup_after_stat_modes)


# Обработчик нажатия кнопки "получить задание" в зависимости от выбранного режима игры
@bot.callback_query_handler(func=lambda callback: callback.data in ['team_mode_task', 'self_mode_task'])
def handle_task_modes(callback):
    if callback.data == 'team_mode_task':
        bot.answer_callback_query(callback.id)
        task_key = random.choice(list(team_mode_tasks.keys()))
        task_text = team_mode_tasks[task_key]
        ch = callback.message.chat.id
        us_id = callback.from_user.id
        datetime = callback.message.date
        mode = 'Командный'
        # Создаем новую клавиатуру
        task_button = types.InlineKeyboardButton(text=task_text, callback_data=f'task:{task_key}')
        change_button = types.InlineKeyboardButton(text='🎲 Поменять задание', callback_data='team_mode_change_task')
        keyboard_team_mode = types.InlineKeyboardMarkup(row_width=1)
        keyboard_team_mode.add(task_button, change_button)
        # добавляем данные в таблицу user_tasks
        query = "INSERT INTO user_tasks (chat_id, user_id, start_session, mode, task_text, is_skip) VALUES (?, ?, ?, ?, ?, ?)"
        values = (ch, us_id, timeconv(datetime), mode, task_text, 0)
        cursor.execute(query, values)
        conn.commit()
        # Добавляем данные о задании в таблицу user_songs
        query2 = 'UPDATE user_songs SET task_text = ? WHERE chat_id = ? AND user_id = ? AND is_skip = ? ' \
                 'AND id = (SELECT MAX(id) FROM user_songs WHERE chat_id = ? AND user_id = ?)'
        values2 = (task_text, ch, us_id, 0, ch, us_id)
        cursor.execute(query2, values2)
        conn.commit()
        bot.send_message(callback.message.chat.id, f'<b>Ваше задание:</b>', parse_mode='html',
                         reply_markup=keyboard_team_mode)
    elif callback.data == 'self_mode_task':
        bot.answer_callback_query(callback.id)
        task_key = random.choice(list(self_mode_tasks.keys()))
        task_text = self_mode_tasks[task_key]
        ch = callback.message.chat.id
        us_id = callback.from_user.id
        datetime = callback.message.date
        mode = 'Индивидуальный'
        # Создаем новую клавиатуру
        task_button = types.InlineKeyboardButton(text=task_text, callback_data='self_mode_go_timer')
        change_button = types.InlineKeyboardButton(text='🎲 Поменять задание', callback_data='self_mode_change_task')
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(task_button, change_button)
        # добавляем данные в таблицу user_tasks
        query = "INSERT INTO user_tasks (chat_id, user_id, start_session, mode, task_text, is_skip) VALUES (?, ?, ?, ?, ?, ?)"
        values = (ch, us_id, timeconv(datetime), mode, task_text, 0)
        cursor.execute(query, values)
        conn.commit()
        # Добавляем данные о задании в таблицу user_songs
        query2 = 'UPDATE user_songs SET task_text = ? WHERE chat_id = ? AND user_id = ? AND is_skip = ? ' \
                 'AND id = (SELECT MAX(id) FROM user_songs WHERE chat_id = ? AND user_id = ?)'
        values2 = (task_text, ch, us_id, 0, ch, us_id)
        cursor.execute(query2, values2)
        conn.commit()
        bot.send_message(callback.message.chat.id, f'<b>Ваше задание:</b>', parse_mode='html', reply_markup=keyboard)


# Обработчик нажатия кнопки "поменять задание"
@bot.callback_query_handler(func=lambda callback: callback.data in ['team_mode_change_task', 'self_mode_change_task'])
def handle_change_task_modes(callback):
    if callback.data == 'self_mode_change_task' and lock:
        bot.answer_callback_query(callback.id)
        ch = callback.message.chat.id
        us_id = callback.from_user.id
        datetime = callback.message.date
        mode = 'Индивидуальный'
        # Если пользователь нажал на "поменять задание", то в таблице user_tasks мы меняем статус is_skip на 1
        update_tasks_and_songs.update_task_status(ch, us_id)
        task_key = random.choice(list(self_mode_tasks.keys()))
        task_text = self_mode_tasks[task_key]
        task_button = types.InlineKeyboardButton(text=task_text, callback_data='self_mode_go_timer')
        change_button = types.InlineKeyboardButton(text='🎲 Поменять задание', callback_data='self_mode_change_task')
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(task_button, change_button)
        # Добавляем новое задание в user_tasks
        update_tasks_and_songs.insert_user_task(ch, us_id, timeconv(datetime), mode, task_text)
        # Меняем задание в таблице user_songs
        query2 = 'UPDATE user_songs SET task_text = ? WHERE chat_id = ? AND user_id = ? AND is_skip = ? ' \
                 'AND id = (SELECT MAX(id) FROM user_songs WHERE chat_id = ? AND user_id = ?)'
        values2 = (task_text, ch, us_id, 0, ch, us_id)
        cursor.execute(query2, values2)
        conn.commit()
        bot.send_message(callback.message.chat.id, f'<b>Ваше задание:</b>', parse_mode='html', reply_markup=keyboard)
    elif callback.data == 'team_mode_change_task':
        bot.answer_callback_query(callback.id)
        ch = callback.message.chat.id
        us_id = callback.from_user.id
        datetime = callback.message.date
        mode = 'Командный'
        # Меняем статус задания, которое поменяли
        update_tasks_and_songs.update_task_status(ch, us_id)
        task_key = random.choice(list(team_mode_tasks.keys()))
        task_text = team_mode_tasks[task_key]
        task_button = types.InlineKeyboardButton(text=task_text, callback_data=f'task:{task_key}')
        change_button = types.InlineKeyboardButton(text='🎲 Поменять задание', callback_data='team_mode_change_task')
        keyboard_team_mode = types.InlineKeyboardMarkup(row_width=1)
        keyboard_team_mode.add(task_button, change_button)
        # добавляем новое задание в таблицу user_tasks
        update_tasks_and_songs.insert_user_task(ch, us_id, timeconv(datetime), mode, task_text)
        # Меняем задание в таблице user_songs
        query2 = 'UPDATE user_songs SET task_text = ? WHERE chat_id = ? AND user_id = ? AND is_skip = ? ' \
                 'AND id = (SELECT MAX(id) FROM user_songs WHERE chat_id = ? AND user_id = ?)'
        values2 = (task_text, ch, us_id, 0, ch, us_id)
        cursor.execute(query2, values2)
        conn.commit()
        bot.send_message(callback.message.chat.id, f'<b>Ваше задание:</b>', parse_mode='html',
                         reply_markup=keyboard_team_mode)


# Обработчик нажатия кнопки "поменять песню"
@bot.callback_query_handler(func=lambda callback: callback.data in ['team_mode_another_song', 'self_mode_another_song'])
def handle_another_songs(callback):
    if callback.data == 'self_mode_another_song':
        bot.answer_callback_query(callback.id)
        us_id = callback.from_user.id
        ch = callback.message.chat.id
        # получаем данные о том, какую песню пользователь хочет поменять
        cursor2 = conn.execute('SELECT song_id FROM user_songs WHERE chat_id = ? AND user_id = ? AND is_skip = ? '
                               'ORDER BY start_session DESC LIMIT 1',
                               (ch, us_id, 0))
        current_song_id = cursor2.fetchone()[0]
        # Добавляем данные о том, что песня пропущена в таблицу user_songs
        update_tasks_and_songs.update_current_song_status(ch, us_id, current_song_id)
        bot.send_message(callback.message.chat.id, 'Вы можете получить песню случайным образом или выбрать определенный жанр '
                         'или временной период (1990-е, 2000-е  и т.д.)',
                         parse_mode='html', reply_markup=markup_get_song_self_mode)
    if callback.data == 'team_mode_another_song':
        bot.answer_callback_query(callback.id)
        us_id = callback.from_user.id
        ch = callback.message.chat.id
        # получаем данные о том, какую песню пользователь хочет поменять
        cursor2 = conn.execute('SELECT song_id FROM user_songs WHERE chat_id = ? AND user_id = ? AND is_skip = ? '
                               'ORDER BY start_session DESC LIMIT 1',
                               (ch, us_id, 0))
        current_song_id = cursor2.fetchone()[0]
        # Добавляем данные о том, что песня пропущена в таблицу user_songs
        update_tasks_and_songs.update_current_song_status(ch, us_id, current_song_id)
        bot.send_message(callback.message.chat.id, 'Вы можете получить песню случайным образом или выбрать определенный жанр '
                         'или временной период (1990-е, 2000-е  и т.д.)',
                         parse_mode='html', reply_markup=markup_get_song_team_mode)


# Обработчик таймера в командном режиме
@bot.callback_query_handler(func=lambda callback: callback.data in ['team_mode_timer60',
                                                                    'team_mode_break_timer', 'team_mode_without_timer'])
def handle_timer_team_mode(callback):
    if callback.data == 'team_mode_timer60':
        bot.answer_callback_query(callback.id)
        bot.send_message(callback.message.chat.id,
                         'Таймер будет обновляться каждые 5 секунд. Если готовы раньше времени, '
                         'нажмите 👇', reply_markup=markup_breaktimer_team_mode)
        threading.Thread(target=start_timer60, args=(callback.message.chat.id,)).start()
    elif callback.data == 'team_mode_break_timer':
        team_mode_user_timers[callback.message.chat.id] = 0
    elif callback.data == 'team_mode_without_timer':
        bot.answer_callback_query(callback.id)
        bot.send_message(callback.message.chat.id, 'Как ваши успехи?', reply_markup=markup_after_timers_team_mode)


# Обработчик перехода к таймеру в индивидуальном режиме
@bot.callback_query_handler(func=lambda callback: callback.data in ['self_mode_go_timer'])
def go_timer__self_mode(callback):
    if callback.data == 'self_mode_go_timer':
        bot.answer_callback_query(callback.id)
        us_id = callback.from_user.id
        ch = callback.message.chat.id
        datetime = callback.message.date
        self_mode_user_pointsChat.self_mode_add_points_chat(user_id=us_id, chat_id=ch, points=0,
                                                            right_attempts=1, false_attempts=0,
                                                            start_date=timeconv(datetime), game_status=1)
        bot.send_message(callback.message.chat.id, 'Можете запустить таймер или сыграть без него',
                         reply_markup=markup_timers_self_mode)


# Обработчик таймера в индивидуальном режиме
@bot.callback_query_handler(func=lambda callback: callback.data in ['self_mode_timer60', 'self_mode_break_timer',
                                                                    'self_mode_without_timer'])
def handle_timer_buttons_self_mode(callback):
    if callback.data == 'self_mode_timer60':
        bot.answer_callback_query(callback.id)
        bot.send_message(callback.message.chat.id,
                         'Таймер будет обновляться каждые 5 секунд. Если готовы раньше времени, '
                         'нажмите 👇', reply_markup=markup_self_mode_breaktimer)
        threading.Thread(target=self_mode_start_timer60, args=(callback.message.chat.id,)).start()
    elif callback.data == 'self_mode_break_timer':
        self_mode_user_timers[callback.message.chat.id] = 0
    elif callback.data == 'self_mode_without_timer':
        bot.answer_callback_query(callback.id)
        bot.send_message(callback.message.chat.id, 'Тот, кто отгадал песню должен нажать 👇',
                         reply_markup=markup_self_mode_after_timers)


# Обработчик получения очков в индивидуальном режиме
@bot.callback_query_handler(func=lambda callback: callback.data in ['right_answer_self_mode', 'wrong_answer_self_mode'])
def inline_points_self_mode(callback):
    if callback.data == 'right_answer_self_mode':
        bot.answer_callback_query(callback.id)
        us_id = callback.from_user.id
        ch = callback.message.chat.id
        datetime = callback.message.date
        # Обновляем данные в таблице user_songs
        query = 'UPDATE user_songs SET points = ? WHERE chat_id = ? AND is_skip = ? ' \
                'AND id = (SELECT MAX(id) FROM user_songs WHERE chat_id = ?)'
        values = (1, ch, 0, ch)
        cursor.execute(query, values)
        conn.commit()
        self_mode_user_pointsChat.self_mode_add_points_chat(user_id=us_id, chat_id=ch, points=1,
                                                            right_attempts=0, false_attempts=0,
                                                            start_date=timeconv(datetime), game_status=1)
        user = callback.from_user.first_name
        bot.send_message(callback.message.chat.id,
                         f'{user}, поздравляем! Вы получаете 1 балл, следующую песню объясняете Вы 👇',
                         reply_markup=markup_get_song_self_mode)
    if callback.data == 'wrong_answer_self_mode':
        bot.answer_callback_query(callback.id)
        us_id = callback.from_user.id
        ch = callback.message.chat.id
        # Обновляем данные в таблице user_songs
        query = 'UPDATE user_songs SET points = ? WHERE chat_id = ? AND is_skip = ? ' \
                'AND id = (SELECT MAX(id) FROM user_songs WHERE chat_id = ?)'
        values = (0, ch, 0, ch)
        cursor.execute(query, values)
        conn.commit()
        user = callback.from_user.first_name
        datetime = callback.message.date
        self_mode_user_pointsChat.self_mode_add_points_chat(user_id=us_id, chat_id=ch, points=0, right_attempts=0,
                                                            false_attempts=1,
                                                            start_date=timeconv(datetime), game_status=1)
        bot.send_message(callback.message.chat.id,
                         f'{user}, не расстраивайтесь! Это было непросто! Выберите человека, '
                         f'который будет объяснять песню следующим 👇',
                         reply_markup=markup_get_song_self_mode)


# Обработчик нажатия кнопок выбора режима игры, который пользователь хочет закончить
@bot.callback_query_handler(func=lambda callback: callback.data in ['finish_self_mode', 'finish_team_mode'])
def inline_finish_modes(callback):
    if callback.data == 'finish_self_mode':
        bot.answer_callback_query(callback.id)
        ch = callback.message.chat.id
        self_mode_chat_points = self_mode_user_pointsChat.self_mode_check_chat(chat_id=ch)
        if self_mode_chat_points is not None:
            bot.send_message(callback.message.chat.id, text=f'''
Спасибо за игру! 
Ваша итоговая статистика за игровую сессию:
<b>Количество отгаданных песен:</b> {self_mode_user_pointsChat.self_mode_get_current_points_chat(chat_id=ch)}''',
                             parse_mode='html')
        else:
            bot.send_message(callback.message.chat.id, 'Нажмите "начать игру" или команду /go')
        sleep(1)
        self_mode_user_pointsChat.self_mode_finish_game_chat(chat_id=ch)
    if callback.data == 'finish_team_mode':
        bot.answer_callback_query(callback.id)
        ch = callback.message.chat.id
        current_attempts = team_mode_user_pointsChat.get_current_attempts_chat(chat_id=ch)
        if current_attempts != 0:
            bot.send_message(callback.message.chat.id, text=f'''
Спасибо за игру! Ваша итоговая статистика за игровую сессию:
<b>Количество попыток:</b> {team_mode_user_pointsChat.get_current_attempts_chat(chat_id=ch)}  
<b>Количество правильных ответов:</b> {team_mode_user_pointsChat.get_current_right_answers_chat(chat_id=ch)}  
<b>Количество очков:</b> {team_mode_user_pointsChat.get_current_points_chat(chat_id=ch)}
            ''', parse_mode='html')
        else:
            bot.send_message(callback.message.chat.id, 'Нажмите "начать игру" или команду /go')
        sleep(1)
        team_mode_user_pointsChat.finish_game_chat(chat_id=ch)


# Обработчик текстового сообщения
@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.send_message(message.chat.id, f'''Выберите одну из команд меню:
/go  Начать игру
/stat  Посмотреть статистику
/finish  Закончить игру
/rules  Почитать правила
''')

# Цикл, позволяющий боту не падать при ошибках
while True:
    try:
        bot.polling(none_stop=True)
    except:
        print('Ошибка')
        logging.error('error: {}'.format(sys.exc_info()[0]))
        time.sleep(5)
