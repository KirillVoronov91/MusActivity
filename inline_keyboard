# В отдельном файле мы создаем классы создания инлайн-кнопок в телеграм боте.

from telebot import types


class Choose_mode_menu_keyboard:
    def __init__(self):
        self.keyboard = types.InlineKeyboardMarkup()
        self.button1 = types.InlineKeyboardButton(text='✊ Каждый сам за себя', callback_data='self_mode')
        self.button2 = types.InlineKeyboardButton(text='🤝 Командный режим', callback_data='team_mode')
        self.button3 = types.InlineKeyboardButton(text='📃 Правила', callback_data='rules')
        self.keyboard.add(self.button1)
        self.keyboard.add(self.button2)
        self.keyboard.add(self.button3)


class RulesKeyboard:
    def __init__(self):
        self.keyboard = types.InlineKeyboardMarkup()
        self.button1 = types.InlineKeyboardButton(text='🎮 Начать игру', callback_data='start_game')
        self.button5 = types.InlineKeyboardButton(text='➡️ Продолжить игру', callback_data='continue')
        self.button3 = types.InlineKeyboardButton(text='📊 Статистика', callback_data='stat')
        self.button4 = types.InlineKeyboardButton(text='🏁 Закончить игру', callback_data='finish')
        self.keyboard.add(self.button1, self.button3)
        self.keyboard.add(self.button5)
        self.keyboard.add(self.button4)


class StatKeyboard:
    def __init__(self):
        self.keyboard = types.InlineKeyboardMarkup()
        self.button1 = types.InlineKeyboardButton(text='🎮 Начать игру', callback_data='start_game')
        self.button5 = types.InlineKeyboardButton(text='➡️ Продолжить игру', callback_data='continue')
        self.button2 = types.InlineKeyboardButton(text='📃 Правила', callback_data='rules')
        self.button4 = types.InlineKeyboardButton(text='🏁 Закончить игру', callback_data='finish')
        self.keyboard.add(self.button1, self.button2)
        self.keyboard.add(self.button5)
        self.keyboard.add(self.button4)


class StatKeyboardModes:
    def __init__(self):
        self.keyboard = types.InlineKeyboardMarkup()
        self.button1 = types.InlineKeyboardButton(text='✊ Каждый сам за себя', callback_data='stat_self_mode')
        self.button2 = types.InlineKeyboardButton(text='🤝 Командный режим', callback_data='stat_team_mode')
        self.button5 = types.InlineKeyboardButton(text='➡️ Продолжить игру', callback_data='continue')
        self.button4 = types.InlineKeyboardButton(text='🏁 Закончить игру', callback_data='finish')
        self.keyboard.add(self.button1)
        self.keyboard.add(self.button2)
        self.keyboard.add(self.button5)
        self.keyboard.add(self.button4)


class AfterStatKeyboardModes:
    def __init__(self):
        self.keyboard = types.InlineKeyboardMarkup()
        self.button5 = types.InlineKeyboardButton(text='➡️ Продолжить игру', callback_data='continue')
        self.button4 = types.InlineKeyboardButton(text='🏁 Закончить игру', callback_data='finish')
        self.keyboard.add(self.button5)
        self.keyboard.add(self.button4)



class Get_song_keyboard_self_mode:
    def __init__(self):
        self.keyboard = types.InlineKeyboardMarkup()
        self.buttonA3 = types.InlineKeyboardButton(text='🎶 Случайная песня', callback_data='self_mode_random_song')
        self.buttonB3 = types.InlineKeyboardButton(text='🎸 Выбрать жанр', callback_data='self_mode_genre')
        self.buttonC3 = types.InlineKeyboardButton(text='📆 Выбрать временной период', callback_data='self_mode_period')
        self.keyboard.row(self.buttonA3)
        self.keyboard.row(self.buttonB3)
        self.keyboard.row(self.buttonC3)


class Get_song_keyboard_team_mode:
    def __init__(self):
        self.keyboard = types.InlineKeyboardMarkup()
        self.buttonA3 = types.InlineKeyboardButton(text='🎶 Случайная песня', callback_data='team_mode_random_song')
        self.buttonB3 = types.InlineKeyboardButton(text='🎸 Выбрать жанр', callback_data='team_mode_genre')
        self.buttonC3 = types.InlineKeyboardButton(text='📆 Выбрать временной период', callback_data='team_mode_period')
        self.keyboard.row(self.buttonA3)
        self.keyboard.row(self.buttonB3)
        self.keyboard.row(self.buttonC3)

class genres_team:
    def __init__(self):
        self.keyboard = types.InlineKeyboardMarkup()
        self.buttonA3 = types.InlineKeyboardButton(text='🎸 Рок', callback_data='rock_song_team')
        self.buttonB3 = types.InlineKeyboardButton(text='🎶 Поп', callback_data='pop_song_team')
        self.buttonC3 = types.InlineKeyboardButton(text='🎼 Барды/эстрада', callback_data='bard_song_team')
        self.buttonD3 = types.InlineKeyboardButton(text='🎤 Хип-хоп, Электронная, RnB', callback_data='rap_song_team')
        self.buttonE3 = types.InlineKeyboardButton(text='🎬 Из фильмов', callback_data='movies_song_team')
        self.keyboard.row(self.buttonA3)
        self.keyboard.row(self.buttonB3)
        self.keyboard.row(self.buttonC3)
        self.keyboard.row(self.buttonD3)
        self.keyboard.row(self.buttonE3)
class genres_self:
    def __init__(self):
        self.keyboard = types.InlineKeyboardMarkup()
        self.buttonA3 = types.InlineKeyboardButton(text='🎸 Рок', callback_data='rock_song_self')
        self.buttonB3 = types.InlineKeyboardButton(text='🎶 Поп', callback_data='pop_song_self')
        self.buttonC3 = types.InlineKeyboardButton(text='🎼 Барды/эстрада', callback_data='bard_song_self')
        self.buttonD3 = types.InlineKeyboardButton(text='🎤 Хип-хоп, Электронная, RnB', callback_data='rap_song_self')
        self.buttonE3 = types.InlineKeyboardButton(text='🎬 Из фильмов', callback_data='movies_song_self')
        self.keyboard.row(self.buttonA3)
        self.keyboard.row(self.buttonB3)
        self.keyboard.row(self.buttonC3)
        self.keyboard.row(self.buttonD3)
        self.keyboard.row(self.buttonE3)


class times_team:
    def __init__(self):
        self.keyboard = types.InlineKeyboardMarkup()
        self.buttonA3 = types.InlineKeyboardButton(text='🎤2020-е', callback_data='2020_song_team')
        self.buttonB3 = types.InlineKeyboardButton(text='🎶 2010-е', callback_data='2010_song_team')
        self.buttonC3 = types.InlineKeyboardButton(text='🎼 2000-е', callback_data='2000_song_team')
        self.buttonD3 = types.InlineKeyboardButton(text='🎸 1990-е', callback_data='1990_song_team')
        self.buttonE3 = types.InlineKeyboardButton(text='☭ Советский союз', callback_data='ussr_song_team')
        self.keyboard.row(self.buttonA3)
        self.keyboard.row(self.buttonB3)
        self.keyboard.row(self.buttonC3)
        self.keyboard.row(self.buttonD3)
        self.keyboard.row(self.buttonE3)

class times_self:
    def __init__(self):
        self.keyboard = types.InlineKeyboardMarkup()
        self.buttonA3 = types.InlineKeyboardButton(text='🎤2020-е', callback_data='2020_song_self')
        self.buttonB3 = types.InlineKeyboardButton(text='🎶 2010-е', callback_data='2010_song_self')
        self.buttonC3 = types.InlineKeyboardButton(text='🎼 2000-е', callback_data='2000_song_self')
        self.buttonD3 = types.InlineKeyboardButton(text='🎸 1990-е', callback_data='1990_song_self')
        self.buttonE3 = types.InlineKeyboardButton(text='☭ Советский союз', callback_data='ussr_song_self')
        self.keyboard.row(self.buttonA3)
        self.keyboard.row(self.buttonB3)
        self.keyboard.row(self.buttonC3)
        self.keyboard.row(self.buttonD3)
        self.keyboard.row(self.buttonE3)

class Timers_keyboard_self_mode:
    def __init__(self):
        self.keyboard = types.InlineKeyboardMarkup()
        self.buttonA4 = types.InlineKeyboardButton(text='⏳ 1 минута', callback_data='self_mode_timer60')
        self.buttonB4 = types.InlineKeyboardButton(text='➡️ Без таймера', callback_data='self_mode_without_timer')
        self.keyboard.row(self.buttonA4)
        self.keyboard.row(self.buttonB4)


class Timers_keyboard_team_mode:
    def __init__(self):
        self.keyboard = types.InlineKeyboardMarkup()
        self.buttonA4 = types.InlineKeyboardButton(text='⏳ 1 минута', callback_data='team_mode_timer60')
        self.buttonB4 = types.InlineKeyboardButton(text='➡️ Без таймера', callback_data='team_mode_without_timer')
        self.keyboard.row(self.buttonA4)
        self.keyboard.row(self.buttonB4)


class Chosen_song_keyboard_self_mode:
    def __init__(self):
        self.keyboard = types.InlineKeyboardMarkup()
        self.buttonA4 = types.InlineKeyboardButton(text='🎲 Получить задание', callback_data='self_mode_task')
        self.buttonB4 = types.InlineKeyboardButton(text='🎶 Другая песня', callback_data='self_mode_another_song')
        self.keyboard.row(self.buttonA4)
        self.keyboard.row(self.buttonB4)


class Chosen_song_keyboard_team_mode:
    def __init__(self):
        self.keyboard = types.InlineKeyboardMarkup()
        self.buttonA4 = types.InlineKeyboardButton(text='🎲 Получить задание', callback_data='team_mode_task')
        self.buttonB4 = types.InlineKeyboardButton(text='🎶 Другая песня', callback_data='team_mode_another_song')
        self.keyboard.row(self.buttonA4)
        self.keyboard.row(self.buttonB4)


class After_timers_keyboard_team_mode:
    def __init__(self):
        self.keyboard = types.InlineKeyboardMarkup()
        self.buttonA5 = types.InlineKeyboardButton(text='🔥 Получилось на 2 балла!)', callback_data='right_answer_2')
        self.buttonB5 = types.InlineKeyboardButton(text='😎 Получилось на 1,5 балла!)', callback_data='right_answer_15')
        self.buttonC5 = types.InlineKeyboardButton(text='😎 Получилось на 1 балл!)', callback_data='right_answer_1')
        self.buttonD5 = types.InlineKeyboardButton(text='🙃 Меня не поняли :(', callback_data='wrong_answer')
        # self.buttonE5 = types.InlineKeyboardButton(text='🔙 Получить новую песню и задание', callback_data='team_mode')
        self.keyboard.row(self.buttonA5)
        self.keyboard.row(self.buttonB5)
        self.keyboard.row(self.buttonC5)
        self.keyboard.row(self.buttonD5)
        # self.keyboard.row(self.buttonE5)


class Self_mode_after_timers_keyboard:
    def __init__(self):
        self.keyboard = types.InlineKeyboardMarkup()
        self.buttonA5 = types.InlineKeyboardButton(text='😎 эту кнопку ', callback_data='right_answer_self_mode')
        self.buttonB5 = types.InlineKeyboardButton(text='🙃 Никто не догадался :(', callback_data='wrong_answer_self_mode')
        # self.buttonC5 = types.InlineKeyboardButton(text='🔙 Получить новую песню и задание', callback_data='self_mode_task')
        self.keyboard.row(self.buttonA5)
        self.keyboard.row(self.buttonB5)
        # self.keyboard.row(self.buttonC5)


class Break_timer_keyboard_team_mode:
    def __init__(self):
        self.keyboard = types.InlineKeyboardMarkup()
        self.buttontimer = types.InlineKeyboardButton(text='Прервать таймер', callback_data='team_mode_break_timer')
        self.keyboard.row(self.buttontimer)


class self_mode_break_timer_keyboard:
    def __init__(self):
        self.keyboard = types.InlineKeyboardMarkup()
        self.buttontimer = types.InlineKeyboardButton(text='Прервать таймер', callback_data='self_mode_break_timer')
        self.keyboard.row(self.buttontimer)


class Finish_keyboard_modes:
    def __init__(self):
        self.keyboard = types.InlineKeyboardMarkup()
        self.button1 = types.InlineKeyboardButton(text='✊ Каждый сам за себя', callback_data='finish_self_mode')
        self.button2 = types.InlineKeyboardButton(text='🤝 Командный режим', callback_data='finish_team_mode')
        self.button5 = types.InlineKeyboardButton(text='➡️ Продолжить игру', callback_data='continue')
        self.keyboard.add(self.button1)
        self.keyboard.add(self.button2)
        self.keyboard.add(self.button5)
