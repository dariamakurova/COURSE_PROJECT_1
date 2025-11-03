import json
import os
import re

from src.utils import open_excel


def services_simple_search(search_str):
    """ Пользователь передает строку для поиска, возвращается JSON-ответ со всеми транзакциями,
    содержащими запрос в описании или категории"""

    transactions_xlsx = os.path.join((os.path.dirname(os.path.dirname(__file__))), "data", "operations.xlsx")
    transactions = open_excel(transactions_xlsx)

    result = [
        transaction
        for transaction in transactions
        if (isinstance(transaction.get("Описание"), str)
           and re.search(search_str, transaction["Описание"], re.IGNORECASE))
           or (isinstance(transaction.get("Категория"), str)
           and re.search(search_str, transaction["Категория"], re.IGNORECASE))
    ]

    return json.dumps(result, sort_keys=False, indent=4, ensure_ascii=False)

if __name__ == "__main__":

    print(services_simple_search("линзомат"))