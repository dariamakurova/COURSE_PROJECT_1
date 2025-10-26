import datetime
import pandas as pd
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

    if total_spent:
        cashback = total_spent / 100
        return round(cashback, 2)
    else:
        return 0


def get_top_5_by_spent(transactions: list[dict]) -> list[dict]:
    """ Функция, которая возвращает топ-5 транзакций по расходам """

    df = pd.DataFrame(transactions)
    df["Сумма платежа"] = pd.to_numeric(df["Сумма платежа"], errors="coerce")
    df = df.dropna(subset=["Сумма платежа"])

    transactions_sorted = df.sort_values(by='Сумма платежа', ascending=True).head(5)
    top_5_transactions = []
    for _, transaction in transactions_sorted.iterrows():
        try:
            date = (datetime.datetime.strptime(transaction["Дата операции"], "%d.%m.%Y %H:%M:%S")).strftime("%d.%m.%Y")
            transaction_info = {"date": date, "amount": transaction.get("Сумма платежа"),
                                "category": transaction.get("Категория"), "description": transaction.get("Описание")}
            top_5_transactions.append(transaction_info)
        except (KeyError, ValueError):
            continue

    return top_5_transactions

# if __name__ == "__main__":
#
#     get_greeting(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#
#     path = os.path.join((os.path.dirname(os.path.dirname(__file__))), "data", "operations.xlsx")
#     transactions = open_excel(path)
#
#     # list_of_last_digits = get_last_digits(transactions)
#     # print(list_of_last_digits)
#     #
#     # for number in list_of_last_digits:
#     #     print (f'{number}: {get_total_spent(transactions, number)} {get_cashback(get_total_spent(transactions, number))}')
#
#     # print (transactions)
#     print(get_top_5_by_spent(transactions))