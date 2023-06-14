# В отдельном файле мы создаем классы, при помощи которых коммуницируем с базой данных. Эти классы импортируются в основной код

import sqlite3
import datetime
import os
project_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
conn = sqlite3.connect(os.path.join(project_root_dir, 'db', 'users_base'), check_same_thread=False)
cursor = conn.cursor()


class UserInfo:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor

    def add_user(self, user_id: int, user_name: str, user_surname: str, username: str):
        self.cursor.execute('INSERT INTO users_info (user_id, user_name, user_surname, username) VALUES (?, ?, ?, ?)', (user_id, user_name, user_surname, username))
        self.conn.commit()


    def add_chat(self, chat_id: int, chat_title: str):
        self.cursor.execute('INSERT INTO chats_info (chat_id, chat_title) VALUES (?, ?)', (chat_id, chat_title))
        self.conn.commit()


class team_mode_UserPointsChat:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor


    def add_points_chat(self, user_id: int, chat_id: int, points: int, attempts: int, right_answers: int, false_answers: int, start_date: datetime, game_status: int):
        self.cursor.execute(
        'INSERT INTO team_mode_chat_users_points (user_id, chat_id, points, start_date, attempts, right_answers, false_answers, game_status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        (user_id, chat_id, points, start_date, attempts, right_answers, false_answers, game_status))
        self.conn.commit()

    def finish_game_chat(self, chat_id: int):
        self.cursor.execute("UPDATE team_mode_chat_users_points SET game_status = 0 WHERE chat_id = ? AND game_status = 1", (chat_id,))
        self.conn.commit()

    def get_points_chat(self, chat_id: int):
        self.cursor.execute("""
                    SELECT users_info.user_name, users_info.user_surname, 
                    SUM(team_mode_chat_users_points.points) as total_points
                    FROM team_mode_chat_users_points
                    LEFT JOIN users_info ON
                    team_mode_chat_users_points.user_id = users_info.user_id
                    WHERE team_mode_chat_users_points.chat_id = ?
                    GROUP BY team_mode_chat_users_points.user_id
               """, (chat_id,))
        points_by_user = self.cursor.fetchall()
        if not points_by_user:
            return 0
        else:
            points_formatted = [f"{name} {surname}: {points}" for name, surname, points in points_by_user]
            return "\n" + "\n".join(points_formatted)

    def get_current_points_chat(self, chat_id: int):
        self.cursor.execute("""
                      SELECT users_info.user_name, users_info.user_surname, 
                      SUM(team_mode_chat_users_points.points) as total_points
                      FROM team_mode_chat_users_points
                      LEFT JOIN users_info ON
                      team_mode_chat_users_points.user_id = users_info.user_id
                      WHERE team_mode_chat_users_points.chat_id = ? AND team_mode_chat_users_points.game_status = 1
                      GROUP BY team_mode_chat_users_points.user_id
                 """, (chat_id,))
        points_by_user = self.cursor.fetchall()
        if not points_by_user:
            return 0
        else:
            points_formatted = [f"{name} {surname}: {points}" for name, surname, points in points_by_user]
            return "\n" + "\n".join(points_formatted)

    def get_attempts_chat(self, chat_id: int):
        self.cursor.execute("""
                      SELECT users_info.user_name, users_info.user_surname, 
                      SUM(team_mode_chat_users_points.attempts) as total_attempts
                      FROM team_mode_chat_users_points
                      LEFT JOIN users_info ON
                      team_mode_chat_users_points.user_id = users_info.user_id
                      WHERE team_mode_chat_users_points.chat_id = ?
                      GROUP BY team_mode_chat_users_points.user_id
                 """, (chat_id,))
        attempts_by_user = self.cursor.fetchall()
        if not attempts_by_user:
            return 0
        else:
            attempts_formatted = [f"{name} {surname}: {attempts}" for name, surname, attempts in attempts_by_user]
            return "\n" + "\n".join(attempts_formatted)

    def get_current_attempts_chat(self, chat_id: int):
        self.cursor.execute("""
                      SELECT users_info.user_name, users_info.user_surname, 
                      SUM(team_mode_chat_users_points.attempts) as total_attempts
                      FROM team_mode_chat_users_points
                      LEFT JOIN users_info ON
                      team_mode_chat_users_points.user_id = users_info.user_id
                      WHERE team_mode_chat_users_points.chat_id = ? AND team_mode_chat_users_points.game_status = 1
                      GROUP BY team_mode_chat_users_points.user_id
                 """, (chat_id,))
        attempts_by_user = self.cursor.fetchall()
        if not attempts_by_user:
            return 0
        else:
            attempts_formatted = [f"{name} {surname}: {attempts}" for name, surname, attempts in attempts_by_user]
            return "\n" + "\n".join(attempts_formatted)

    def get_current_right_answers_chat(self, chat_id: int):
        self.cursor.execute("""
                      SELECT users_info.user_name, users_info.user_surname, 
                      SUM(team_mode_chat_users_points.right_answers) as total_right_answers
                      FROM team_mode_chat_users_points
                      LEFT JOIN users_info ON
                      team_mode_chat_users_points.user_id = users_info.user_id
                      WHERE team_mode_chat_users_points.chat_id = ? AND team_mode_chat_users_points.game_status = 1
                      GROUP BY team_mode_chat_users_points.user_id
                 """, (chat_id,))
        right_answers_by_user = self.cursor.fetchall()
        if not right_answers_by_user:
            return 0
        else:
            right_answers_formatted = [f"{name} {surname}: {right_answers}" for name, surname, right_answers in right_answers_by_user]
            return "\n" + "\n".join(right_answers_formatted)

    def get_right_answers_chat(self, chat_id: int):
        self.cursor.execute("""
                        SELECT users_info.user_name, users_info.user_surname, 
                        SUM(team_mode_chat_users_points.right_answers) as total_right_answers
                        FROM team_mode_chat_users_points
                        LEFT JOIN users_info ON
                        team_mode_chat_users_points.user_id = users_info.user_id
                        WHERE team_mode_chat_users_points.chat_id = ?
                        GROUP BY team_mode_chat_users_points.user_id
                   """, (chat_id,))
        right_answers_by_user = self.cursor.fetchall()
        if not right_answers_by_user:
            return 0
        else:
            right_answers_formatted = [f"{name} {surname}: {right_answers}" for name, surname, right_answers in
                                       right_answers_by_user]
            return "\n" + "\n".join(right_answers_formatted)


class self_mode_UserPointsChat:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor

    def self_mode_add_points_chat(self, user_id: int, chat_id: int, points: int, right_attempts: int, false_attempts: int, start_date: datetime, game_status: int):
        self.cursor.execute(
        'INSERT INTO self_mode_chat_users_points (user_id, chat_id, points, start_date, right_attempts, false_attempts, game_status) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (user_id, chat_id, points, start_date, right_attempts, false_attempts, game_status))
        self.conn.commit()

    def self_mode_finish_game_chat(self, chat_id: int):
        self.cursor.execute("UPDATE self_mode_chat_users_points SET game_status = 0 WHERE chat_id = ? AND game_status = 1", (chat_id,))
        self.conn.commit()

    def self_mode_check_chat(self, chat_id: int):
        self.cursor.execute("""
                       SELECT 
                       SUM(self_mode_chat_users_points.points) as total_points
                       FROM self_mode_chat_users_points
                       LEFT JOIN users_info ON
                       self_mode_chat_users_points.user_id = users_info.user_id
                       WHERE self_mode_chat_users_points.chat_id = ? AND game_status = 1
                       
                  """, (chat_id,))
        points_by_user = self.cursor.fetchall()[0][0]
        return points_by_user

    def self_mode_get_points_chat(self, chat_id: int):
        self.cursor.execute("""
                    SELECT users_info.user_name, users_info.user_surname,
                    SUM(self_mode_chat_users_points.points) as total_points
                    FROM self_mode_chat_users_points
                    LEFT JOIN users_info ON
                    self_mode_chat_users_points.user_id = users_info.user_id
                    WHERE self_mode_chat_users_points.chat_id = ?
                    GROUP BY self_mode_chat_users_points.user_id
               """, (chat_id,))
        points_by_user = self.cursor.fetchall()
        if not points_by_user:
            return 0
        else:
            points_formatted = [f"{name} {surname}: {points}" for name, surname, points in points_by_user]
            return "\n" + "\n".join(points_formatted)

    def self_mode_get_current_points_chat(self, chat_id: int):
        self.cursor.execute("""
                      SELECT users_info.user_name, users_info.user_surname,
                      SUM(self_mode_chat_users_points.points) as total_points
                      FROM self_mode_chat_users_points
                      LEFT JOIN users_info ON
                      self_mode_chat_users_points.user_id = users_info.user_id
                      WHERE self_mode_chat_users_points.chat_id = ? AND self_mode_chat_users_points.game_status = 1
                      GROUP BY self_mode_chat_users_points.user_id
                 """, (chat_id,))
        points_by_user = self.cursor.fetchall()
        if not points_by_user:
            return 0
        else:
            points_formatted = [f"{name} {surname}: {points}" for name, surname, points in points_by_user]
            return "\n" + "\n".join(points_formatted)

class Songs:
    def __init__(self, cursor):
        self.conn = conn
        self.cursor = cursor

    def insert_song_to_db(self, chat_id, user_id, start_session, song_id):
        self.cursor.execute(
            'INSERT INTO user_songs (chat_id, user_id, start_session, song_id, is_skip) VALUES (?, ?, ?, ?, ?)',
            (chat_id, user_id, start_session, song_id, 0))
        self.conn.commit()

    def insert_genre_to_db(self, chat_id, user_id, start_session, genre):
        self.cursor.execute(
            'INSERT INTO genres (chat_id, user_id, start_session, genre) VALUES (?, ?, ?, ?)',
            (chat_id, user_id, start_session, genre))
        self.conn.commit()

    def insert_times_to_db(self, chat_id, user_id, start_session, times):
        self.cursor.execute(
            'INSERT INTO times (chat_id, user_id, start_session, times) VALUES (?, ?, ?, ?)',
            (chat_id, user_id, start_session, times))
        self.conn.commit()

    def get_random_song(self):
        self.cursor.execute('SELECT singer, title, texts, author, song_id, video FROM songs ORDER BY RANDOM() LIMIT 1;')
        song = self.cursor.fetchone()
        formatted_song = f'<b>{song[0]} \n"{song[1]}"</b>\n\n{song[2]}\n\n<b>Автор:</b> {song[3]}\n\n\n  {song[5]}'
        return tuple((song[4], formatted_song))  # возвращаем кортеж с номером песни и отформатированным текстом


    def get_song_rock(self, chat_id: int, user_id: int, start_session: datetime):
        try:
            self.cursor.execute('SELECT singer, title, texts, author, song_id, video FROM songs WHERE genre = "Рок" ORDER BY RANDOM() LIMIT 1;')
            song = self.cursor.fetchone()
            self.cursor.execute('INSERT INTO user_songs (chat_id, user_id, start_session, song_id) VALUES (?, ?, ?, ?)',
                                (chat_id, user_id, start_session, song[4]))
            self.conn.commit()
            formatted_song = f'<b>{song[0]} \n"{song[1]}"</b>\n\n{song[2]}\n\n<b>Автор:</b> {song[3]}\n\n\n {song[5]}'
            return formatted_song
        except Exception as e:
            print(e)
            return None

    def get_song_pop(self, chat_id: int, user_id: int, start_session: datetime):
        try:
            self.cursor.execute('SELECT singer, title, texts, author, song_id, video FROM songs WHERE genre = "Поп" ORDER BY RANDOM() LIMIT 1;')
            song = self.cursor.fetchone()
            self.cursor.execute('INSERT INTO user_songs (chat_id, user_id, start_session, song_id) VALUES (?, ?, ?, ?)',
                                (chat_id, user_id, start_session, song[4]))
            self.conn.commit()
            formatted_song = f'<b>{song[0]} \n"{song[1]}"</b>\n\n{song[2]}\n\n<b>Автор:</b> {song[3]}\n\n\n {song[5]}'
            return formatted_song
        except Exception as e:
            print(e)
            return None
    def get_song_bards(self, chat_id: int, user_id: int, start_session: datetime):
        try:
            self.cursor.execute('SELECT singer, title, texts, author, song_id, video FROM songs WHERE genre = "Барды, эстрада" ORDER BY RANDOM() LIMIT 1;')
            song = self.cursor.fetchone()
            self.cursor.execute('INSERT INTO user_songs (chat_id, user_id, start_session, song_id) VALUES (?, ?, ?, ?)',
                                (chat_id, user_id, start_session, song[4]))
            self.conn.commit()
            formatted_song = f'<b>{song[0]} \n"{song[1]}"</b>\n\n{song[2]}\n\n<b>Автор:</b> {song[3]}\n\n\n{song[5]}'
            return formatted_song
        except Exception as e:
            print(e)
            return None

    def get_song_movies(self, chat_id: int, user_id: int, start_session: datetime):
        try:
            self.cursor.execute(
                'SELECT singer, title, texts, author, song_id, video FROM songs WHERE genre = "Из фильмов и мультфильмов" ORDER BY RANDOM() LIMIT 1;')
            song = self.cursor.fetchone()
            self.cursor.execute('INSERT INTO user_songs (chat_id, user_id, start_session, song_id) VALUES (?, ?, ?, ?)',
                                (chat_id, user_id, start_session, song[4]))
            self.conn.commit()
            formatted_song = f'<b>{song[0]} \n"{song[1]}"</b>\n\n{song[2]}\n\n<b>Автор:</b> {song[3]}\n\n\n {song[5]}'
            return formatted_song
        except Exception as e:
            print(e)
            return None

    def get_song_hip(self, chat_id: int, user_id: int, start_session: datetime):
        try:
            self.cursor.execute(
                'SELECT singer, title, texts, author, song_id, video FROM songs WHERE genre = "Хип-хоп, Rnb, Рэп" or genre = "Электронная музыка" ORDER BY RANDOM() LIMIT 1;')
            song = self.cursor.fetchone()
            self.cursor.execute('INSERT INTO user_songs (chat_id, user_id, start_session, song_id) VALUES (?, ?, ?, ?)',
                                (chat_id, user_id, start_session, song[4]))
            self.conn.commit()
            formatted_song = f'<b>{song[0]} \n"{song[1]}"</b>\n\n{song[2]}\n\n<b>Автор:</b> {song[3]}\n\n\n {song[5]}'
            return formatted_song
        except Exception as e:
            print(e)
            return None


    def get_song_ussr(self, chat_id: int, user_id: int, start_session: datetime):
        try:
            self.cursor.execute(
                'SELECT singer, title, texts, author, song_id, video FROM songs WHERE times = "Советский Союз" ORDER BY RANDOM() LIMIT 1;')
            song = self.cursor.fetchone()
            self.cursor.execute('INSERT INTO user_songs (chat_id, user_id, start_session, song_id) VALUES (?, ?, ?, ?)',
                                (chat_id, user_id, start_session, song[4]))
            self.conn.commit()
            formatted_song = f'<b>{song[0]} \n"{song[1]}"</b>\n\n{song[2]}\n\n<b>Автор:</b> {song[3]}\n\n\n{song[5]}'
            return formatted_song
        except Exception as e:
            print(e)
            return None

    def get_song_90(self, chat_id: int, user_id: int, start_session: datetime):
        try:
            self.cursor.execute(
                'SELECT singer, title, texts, author, song_id, video FROM songs WHERE times = "1990-е" ORDER BY RANDOM() LIMIT 1;')
            song = self.cursor.fetchone()
            self.cursor.execute('INSERT INTO user_songs (chat_id, user_id, start_session, song_id) VALUES (?, ?, ?, ?)',
                                (chat_id, user_id, start_session, song[4]))
            self.conn.commit()
            formatted_song = f'<b>{song[0]} \n"{song[1]}"</b>\n\n{song[2]}\n\n<b>Автор:</b> {song[3]}\n\n\n {song[5]}'
            return formatted_song
        except Exception as e:
            print(e)
            return None

    def get_song_00(self, chat_id: int, user_id: int, start_session: datetime):
        try:
            self.cursor.execute(
                'SELECT singer, title, texts, author, song_id, video FROM songs WHERE times = "2000-е" ORDER BY RANDOM() LIMIT 1;')
            song = self.cursor.fetchone()
            self.cursor.execute('INSERT INTO user_songs (chat_id, user_id, start_session, song_id) VALUES (?, ?, ?, ?)',
                                (chat_id, user_id, start_session, song[4]))
            self.conn.commit()
            formatted_song = f'<b>{song[0]} \n"{song[1]}"</b>\n\n{song[2]}\n\n<b>Автор:</b> {song[3]}\n\n\n {song[5]}'
            return formatted_song
        except Exception as e:
            print(e)
            return None

    def get_song_10(self, chat_id: int, user_id: int, start_session: datetime):
        try:
            self.cursor.execute(
                'SELECT singer, title, texts, author, song_id, video FROM songs WHERE times = "2010-е" ORDER BY RANDOM() LIMIT 1;')
            song = self.cursor.fetchone()
            self.cursor.execute('INSERT INTO user_songs (chat_id, user_id, start_session, song_id) VALUES (?, ?, ?, ?)',
                                (chat_id, user_id, start_session, song[4]))
            self.conn.commit()
            formatted_song = f'<b>{song[0]} \n"{song[1]}"</b>\n\n{song[2]}\n\n<b>Автор:</b> {song[3]}\n\n\n {song[5]}'
            return formatted_song
        except Exception as e:
            print(e)
            return None

    def get_song_20(self, chat_id: int, user_id: int, start_session: datetime):
        try:
            self.cursor.execute(
                'SELECT singer, title, texts, author, song_id, video FROM songs WHERE times = "2020-е" ORDER BY RANDOM() LIMIT 1;')
            song = self.cursor.fetchone()
            self.cursor.execute('INSERT INTO user_songs (chat_id, user_id, start_session, song_id) VALUES (?, ?, ?, ?)',
                                (chat_id, user_id, start_session, song[4]))
            self.conn.commit()
            formatted_song = f'<b>{song[0]} \n"{song[1]}"</b>\n\n{song[2]}\n\n<b>Автор:</b> {song[3]}\n\n\n {song[5]}'
            return formatted_song
        except Exception as e:
            print(e)
            return None

class update_tasks_and_songs:

    def __init__(self, cursor):
        self.conn = conn
        self.cursor = cursor

    # метод обновления статуса текущей песни в базе данных
    def update_current_song_status(self, chat_id, user_id, current_song_id):
        self.cursor.execute(
            'UPDATE user_songs SET is_skip = ? WHERE chat_id = ? AND user_id = ? AND song_id = ?',
            (1, chat_id, user_id, current_song_id))
        self.conn.commit()

    def update_task_status(self, chat_id: int, user_id: int):
        self.cursor.execute("UPDATE user_tasks SET is_skip = ? WHERE chat_id = ? AND user_id = ? AND is_skip = ? "
                            "AND id = (SELECT MAX(id) FROM user_tasks WHERE chat_id = ? AND user_id = ?)", (1, chat_id, user_id, 0, chat_id, user_id))
        self.conn.commit()

    def insert_user_task(self, chat_id: int, user_id: int, start_session: datetime,  mode: str, task_text: str):
        query = "INSERT INTO user_tasks (chat_id, user_id, start_session, mode, task_text, is_skip) VALUES (?, ?, ?, ?, ?, ?)"
        values = (chat_id, user_id, start_session, mode, task_text, 0)
        self.cursor.execute(query, values)
        self.conn.commit()

