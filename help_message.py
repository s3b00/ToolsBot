help_message = """
    Привет, меня зовут ToolBot, моя текущая версия -- 0.9.2, давай узнаем, что я могу\n\n
    Мои комманды: \n
     /t_echo -- передаю вам привет!
     /t_mute [user] [time] -- добавляю пользователя в черный список (не может писать в чат), третьим параметром можно написать время в минутах для мута
     /t_unmute [user] -- убираю пользователя из черного списка
     /t_ban [user] -- пользователь исключается из беседы, вернуть его может только администратор беседы
     /t_roullete [limit=6] [target=mute] -- начинаю регистрацию на русскую рулетку с количеством игроков (по умолчанию 6) и целью игры (по умолчанию мут, может быть mute/kick/ban/warn)
     /t_register_roullete -- регистрирует игрока в текущей запущенной игре рулетке
     /t_start_roullete -- начинаю розыгрыш барабана револьвера 
     /t_players_roullete -- выводит текущий список игроков в русскую рулетку
     /t_end_blacklist -- завершает текущую игру в рулетку
     /t_number -- выдает случайный факт о случайном числе
     /t_random -- случайно число в диапазоне от 0 до 100
     /t_flip -- бросок монеты
     /t_suicide -- добавить самого себя в черный список 
     /t_[animal] -- отправляет изображение в текстовом формате (вместо animal может быть goose/elephant/shrek/fak/kchau/yes/face/anime_bitch
     /t_marvel_charters [hero] -- описание персонажа Marvel на русском
     /t_marvel_comics [hero] -- описание комикса Marvel на русском
     /t_weather [city] -- дает приблизительную погоду в городе city 
     /t_pidors -- регистрирует беседу в игре "Пидор дня" 
     /t_start_pidors -- запускает игру "Пидор дня" на сегодняшний день 
     /t_stats_pidors -- выводит статистику игр в "Пидор дня" 
     /t_set [key] [value] -- закрепляет по значению key сообщение value 
     /t_get [key] -- получает сообщение по ключу key
     /t_remove [key] -- удаляет ключ key 
     /t_currency_rates  -- сводка курсов валют
     /t_commands_limit [value] -- устанавливает в беседе лимит комманд за одно сообщение
     /t_report [message] -- отправляет сообщение о жалобе/предложении/баге прямо разработчику
     /t_ping -- пинг all
"""