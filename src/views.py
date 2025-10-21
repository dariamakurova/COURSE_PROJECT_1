import datetime
import re
# import os
# from utils import open_excel

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

    try: card_transactions = [transaction
                         for transaction in transactions
                         if isinstance(transaction.get("Номер карты"), str)
                         and re.search(last_digits, transaction["Номер карты"], re.IGNORECASE)]
    except KeyError

    total_spent = sum([card_transaction["Сумма платежа"] * (-1)
                       for card_transaction
                       in card_transactions
                       if card_transaction.get("Сумма платежа") and int(card_transaction["Сумма платежа"]) < 0])

    return total_spent


# if __name__ == "__main__":
#
#     get_greeting(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#
#     path = os.path.join((os.path.dirname(os.path.dirname(__file__))), "data", "operations.xlsx")
#     transactions = open_excel(path)
#
#     list_of_last_digits = get_last_digits(transactions)
#     print(list_of_last_digits)
#
#     for number in list_of_last_digits:
#         print (f'{number}: {get_total_spent(transactions, number)}')
