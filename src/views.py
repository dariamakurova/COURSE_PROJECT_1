import datetime
import re
import os
from utils import open_excel

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


def get_last_digits(transactions: list[dict]) -> list:
    """ Получение последних списка уникальных номеров карт в виде 4 цифр номера карты из списка транзакции """

    list_of_numbers = []
    for transaction in transactions:
        if (isinstance(transaction.get("Номер карты"), str)
                and transaction["Номер карты"][-4:] not in list_of_numbers):
            last_digits = transaction["Номер карты"][-4:]
            list_of_numbers.append(last_digits)

    return list_of_numbers

def get_total_spent(transactions: list[dict], last_digits: str) -> float:
    """ Подсчет общей суммы расходов по заданной карте """

    total_spent = 0.0

    for transaction in transactions:
        card_number = transaction.get("Номер карты")
        amount = transaction.get("Сумма платежа")

        if isinstance(card_number, str) and card_number.endswith(last_digits):
            try:
                value = float(str(amount).replace(',', '.'))
                if value < 0:  # учитываем только расходы
                    total_spent += abs(value)
            except (TypeError, ValueError):
                continue

    return round(total_spent, 2)

def get_cashback(total_spent: float) -> float:
    """ Расчет кэшбека - 1 руб. за каждые потраченные 100 руб."""

    cashback = total_spent / 100

    return round(cashback, 2)

if __name__ == "__main__":

    get_greeting(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    path = os.path.join((os.path.dirname(os.path.dirname(__file__))), "data", "operations.xlsx")
    transactions = open_excel(path)

    list_of_last_digits = get_last_digits(transactions)
    print(list_of_last_digits)

    for number in list_of_last_digits:
        print (f'{number}: {get_total_spent(transactions, number)} {get_cashback(get_total_spent(transactions, number))}')
