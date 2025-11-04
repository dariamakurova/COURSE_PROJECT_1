import json
import logging
import datetime
import os
from locale import currency

from dotenv import load_dotenv
import requests
import pandas as pd

utils_logger = logging.getLogger("utils_logger")
logger_file = os.path.join((os.path.dirname(os.path.dirname(__file__))), "data", "utils.log")
utils_handler = logging.FileHandler(logger_file, mode="w")
utils_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
utils_handler.setFormatter(utils_formatter)
utils_logger.addHandler(utils_handler)
utils_logger.setLevel(logging.DEBUG)


def open_excel(file: str) -> list[dict]:
    """Получение данных из .xlsx файла"""
    if os.path.exists(file):
        utils_logger.info("Проверка наличия файла с данными")
        try:
            transactions = pd.read_excel(file).to_dict(orient="records")
            utils_logger.info("Чтение данных из файла")
        except ValueError as e:
            utils_logger.error("Ошибка получения данных")
            return []
    else:
        utils_logger.error("Файл не найден")
        return []
    return transactions

def get_transactions_for_period(date: str, transactions: list) -> list:
    """ Функция, которая фильтрует транзации на текущий месяц от заданной даты """

    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    utils_logger.info("Обработка входящей даты")
    start_date = date_obj.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    filtered_transactions = []
    for transaction in transactions:
        transaction_date_str = transaction.get("Дата операции")
        if not transaction_date_str:
            continue

        try:
            transaction_date = datetime.datetime.strptime(transaction_date_str, "%d.%m.%Y %H:%M:%S")
        except ValueError:
            utils_logger.error("Некорректный формат даты в транзакции")
            continue

        if start_date <= transaction_date < date_obj:
            filtered_transactions.append(transaction)

        utils_logger.info("Сформирован список трназакций за указанный период")

    return filtered_transactions


def get_greeting(date_string: str) -> str:
    """  Функция, которая аринимает на вход строку с датой и временем в формате YYYY-MM-DD HH:MM:SS
     и возвращает приветствие «Доброе утро» / «Добрый день» / «Добрый вечер» / «Доброй ночи»
     в зависимости от текущего времени. """

    date_obj = datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    utils_logger.info("Обработка даты")

    if 0 <= date_obj.hour < 6:
        greeting = "Доброй ночи"
    elif 6 <= date_obj.hour < 12:
        greeting = "Доброе утро"
    elif 12 <= date_obj.hour < 18:
        greeting = "Добрый день"
    else:
        greeting = "Добрый вечер"

    utils_logger.info("Выдача приветствия")
    return greeting


def get_last_digits(transactions: list[dict]) -> list:
    """ Получение  списка уникальных номеров карт в виде 4 цифр номера карты из списка транзакций """

    list_of_numbers = []
    for transaction in transactions:
        try:
            transaction.get("Номер карты")
            utils_logger.info("Поиск номеров карт")
            if (isinstance(transaction.get("Номер карты"), str)
                and transaction["Номер карты"][-4:] not in list_of_numbers):
                last_digits = transaction["Номер карты"][-4:]
                list_of_numbers.append(last_digits)
        except KeyError:
            utils_logger.error("Информация о картах не найдена")
    utils_logger.info("Список уникальных номеров карт с 4-мя последними цифрами сформирован")
    return list_of_numbers

def get_total_spent(transactions: list[dict], last_digits: str) -> float:
    """ Подсчет общей суммы расходов по заданной карте """

    total_spent = 0.0

    for transaction in transactions:
        card_number = transaction.get("Номер карты")
        amount = transaction.get("Сумма платежа")

        if isinstance(card_number, str) and card_number.endswith(last_digits):
            utils_logger.info("Проверка наличия информации о карте")
            try:
                value = float(str(amount).replace(',', '.'))
                if value < 0:  # учитываем только расходы
                    total_spent += abs(value)
            except (TypeError, ValueError):
                utils_logger.error("Ошибка данных")
                continue
            utils_logger.info("Общая сумма расходов по карте посчитана")
        else:
            utils_logger.info("Несуществующая карта")
    return round(total_spent, 2)

def get_cashback(total_spent: float) -> float:
    """ Расчет кэшбека - 1 руб. за каждые потраченные 100 руб."""

    if total_spent:
        utils_logger.info("Расчет кэшбека")
        cashback = total_spent / 100
        utils_logger.info("Кэшбек посчитан")
        return round(cashback, 2)
    else:
        utils_logger.error("Нет данных о расходах")
        return 0


def get_top_5_by_spent(transactions: list[dict]) -> list[dict]:
    """ Функция, которая возвращает топ-5 транзакций по расходам """

    if transactions:
        df = pd.DataFrame(transactions)
        df["Сумма платежа"] = pd.to_numeric(df["Сумма платежа"], errors="coerce")
        df = df.dropna(subset=["Сумма платежа"])
        utils_logger.info("Сотрируем транзакции по сумме платежа по убыванию")
        transactions_sorted = df.sort_values(by='Сумма платежа', ascending=True).head(5)
        utils_logger.info("Формируем список топ-5 по расходам")
        top_5_transactions = []
        for _, transaction in transactions_sorted.iterrows():
            try:
                utils_logger.info("Получаем сведения о транзакциях")
                date = (datetime.datetime.strptime(transaction["Дата операции"], "%d.%m.%Y %H:%M:%S")).strftime("%d.%m.%Y")
                transaction_info = {"date": date, "amount": transaction.get("Сумма платежа"),
                                    "category": transaction.get("Категория"), "description": transaction.get("Описание")}
                top_5_transactions.append(transaction_info)
            except KeyError:
                utils_logger.error("Ошибка получения данных о транзакции")
                continue
        utils_logger.info("Список топ-5 транзакций сформирован")
    else:
        top_5_transactions = []
    return top_5_transactions


def get_currency_rates(currency_code: str) -> float | None:
    "Получение курса обмена валюты"

    load_dotenv()
    EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")
    API_KEY = EXCHANGE_API_KEY

    try:
        utils_logger.info("Получение данных о курсах")
        url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{currency_code}'
        response = requests.get(url)
        return float(response.json()["conversion_rates"]["RUB"])
    except requests.exceptions.RequestException:
        utils_logger.error("Ошибка получения данных о курсах обмена валюты")
        return None




def get_stock_price(company_code: str) -> float | None:
    """ Получение стоимости акций компании """

    load_dotenv()
    SP500_API_KEY = os.getenv("SP500_API_KEY")
    API_KEY = SP500_API_KEY

    try:
        utils_logger.info("Запрос котировок")
        url = f"https://finnhub.io/api/v1/quote?symbol={company_code}&token={API_KEY}"
        response = requests.get(url)
        response =  response.json()
        utils_logger.info("Котировки получены")
        return float(response['c'])
    except requests.exceptions.RequestException:
        utils_logger.error("Ошибка получения котировок")
        return None


def get_user_currencies(file) -> list:
    """ Получение пользовательских настроек для валют """

    try:
        with open(file) as f:
            try:
                data = json.load(f)
                try:
                    user_currencies = data["user_currencies"]
                    if isinstance(user_currencies, list):
                        utils_logger.info("Получены настройки валют пользователя")
                        return user_currencies
                except KeyError:
                    utils_logger.error("Отсутствуют данные или неверный формат")
                    return[]
                except TypeError:
                    utils_logger.error("Отсутствуют данные или неверный формат")
                    return []
            except json.JSONDecodeError:
                utils_logger.error("Ошибка форматирования json файла")
                return []
    except FileNotFoundError:
        utils_logger.error("Файл не найден")
        return []



def get_user_stocks(file) -> list:
    """ Получение пользовательских настроек для котировок """

    try:
        with open(file) as f:
            try:
                data = json.load(f)
                try:
                    user_currencies = data["user_stocks"]
                    if isinstance(user_currencies, list):
                        utils_logger.info("Получены настройки котировок пользователя")
                        return user_currencies
                except KeyError:
                    utils_logger.error("Отсутствуют данные или неверный формат")
                    return []
                except TypeError:
                    utils_logger.error("Отсутствуют данные или неверный формат")
                    return []
            except json.JSONDecodeError:
                utils_logger.error("Ошибка форматирования json файла")
                return []
    except FileNotFoundError:
        utils_logger.error("Файл не найден")
        return []

def get_cards_info(transactions: list[dict]) -> list:
    """ Собирает информацию по картам: последние 4 цифры, общая сумма расходов, кэшбек"""

    cards = get_last_digits(transactions)
    cards_info = []
    for card in cards:
        cards_info.append({"last_digits": card,
                          "total_spent": get_total_spent(transactions, str(card)),
                           "cashback": get_cashback(get_total_spent(transactions, str(card)))})
    return cards_info


def get_currency_rates_list(file) -> list:
    """ Собирает список словарей с информацией о курсе обмена валют """

    user_currencies = get_user_currencies(file)
    currency_rates = []

    for user_currency in user_currencies:
        currency_rates.append({"currency": user_currency, "rate": get_currency_rates(user_currency)})

    return currency_rates


def get_stocks_prices_list(file) -> list:
    """ Собирает список словарей с информацией о котировках """

    user_stocks = get_user_stocks(file)
    stocks_prices = []

    for user_stock in user_stocks:
      stocks_prices.append({"stock": user_stock, "price": get_stock_price(user_stock)})

    return stocks_prices


def transfer_into_dataframe(transactions_list: list) -> pd.DataFrame:
    """ Функция, которая преобразует список транзакций в DataFrame """
    try:
        df = pd.DataFrame(transactions_list)
        return df
    except Exception as e:
        utils_logger.error(f"Ошибка преобразования файла: {e}")




if __name__ == "__main__":

    date = "2021-12-05 22:12:11"
    transactions_xlsx = os.path.join((os.path.dirname(os.path.dirname(__file__))), "data", "operations.xlsx")
    all_transactions = open_excel(transactions_xlsx)
    transactions = get_transactions_for_period(date, all_transactions)

    print(get_top_5_by_spent(transactions))