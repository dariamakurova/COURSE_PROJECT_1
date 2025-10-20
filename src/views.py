import datetime

def get_greeting(date_string: str) -> str:
    """  Функция, которая аринимает на вход строку с датой и временем в формате YYYY-MM-DD HH:MM:SS
     и возвращает приветствие «Доброе утро» / «Добрый день» / «Добрый вечер» / «Доброй ночи»
     в зависимости от текущего времени. """

    date_obj = datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")

    if 0 <= date_obj.hour < 6:
        greeting = "Доброй ночи"
    elif 6 <= date_obj.hour < 12:
        greeting = "Доброе утро"
    elif 12 <= date_obj.hour < 18:
        greeting = "Добрый день"
    else:
        greeting = "Добрый вечер"

    return greeting


if __name__ == "__main__":
    pass