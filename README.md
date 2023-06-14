# MusActivity <img src="Лого Музактивити.png" width="148">
Настольная игра, реализованная в формате телеграм-бота


## Суть игры: 
Игроки при помощи телеграм-бота получают текст известной песни и задание, при помощи которого её надо объяснить остальным участникам игры.

### Как реализовано?

1. Создаём бота в ![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white).
2. Делаем базу данных в ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white), разрабатываем её архитектуру под необходимые нам статистические данные.
3. Пишем на ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) код, создаем инлайн-клавиаутуру, прописываем команды взаимодействия пользователей с ботом, формулируем SQL-запросы, вытягивающие данные из БД, а также пополняющие и меняющие её. 
4. Выкладываем на ![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white) для размещения на контейнерном хостинге - самом простом варианте автономной работы бота.

### Как это выглядит?
- Пользователь инициирует чат с ботом. Чтобы поиграть с друзьями, надо создать общий чат и добавить бота туда.
- Выбирается режим игры (каждый сам за себя или командный).
<p float="left">
  <img src="pics/1.jpg" width="270" />
  <img src="pics/2.jpg" width="270" /> 
  <img src="pics/3.jpg" width="270" />
</p>

- Игроки по очереди получают песню в личные сообщения (помимо текста песни присылается ссылка на Youtube - можно сразу же послушать песню, если не знаешь её).
- После получения песни, игрок в общий чат получает задание, с помощью которого надо её объяснить. Задания (как и песни) можно менять.
- В боте реализована функция таймера, но его можно пропустить или прервать.
- После таймера тот, кто нажал угадал должен нажать кнопку и получить балл, который уходит в таблицу БД с очками пользователей.
<p float="left">
  <img src="pics/4.jpg" width="270" />
  <img src="pics/5.jpg" width="270" /> 
  <img src="pics/6.jpg" width="270" />
</p>

### Как реализована база данных? 
<p><img src="pics/8.png" width="300" height="360" align="left" /</p>
<br>
<p> В базе 9 таблиц: <br>
1. Таблица с информацией по чатам <br>
2. Таблица "жанры" - в ней фиксируется выбор определенного жанра пользователями  <br>
3. Таблица со статистикой очков в индивидуальном режиме <br>  
4. Таблица с песнями - в ней указан автор, исполнитель, текст, жанр, временной период, ссылка на YouTube <br>    
5. Таблица со статистикой очков в командном режиме <br>    
6. Таблица "времена" - в ней фиксируется выбор определенного временного периода пользователями  <br> 
7. Таблица "песни пользователей" - в ней фиксируется путь пользователя - получение песни (её смена), определение задания, начисление баллов  <br>
8. Таблица "задания пользователей" - в ней фиксируется то, какие задания получают пользователи, какие они меняют <br>
9. Таблица с информацией о пользователях
</p>
<br><br>
