import json
import logging
import os
import re


services_logger = logging.getLogger("services_logger")
logger_file = os.path.join((os.path.dirname(os.path.dirname(__file__))), "data", "services.log")
services_handler = logging.FileHandler(logger_file, mode="w")
services_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
services_handler.setFormatter(services_formatter)
services_logger.addHandler(services_handler)
services_logger.setLevel(logging.DEBUG)


def services_simple_search(search_str: str, transactions: list[dict]) -> str:
    """Пользователь передает строку для поиска, возвращается JSON-ответ со всеми транзакциями,
    содержащими запрос в описании или категории"""

    services_logger.info("Поиск соответствующих транзакций")
    result = []
    try: result = [
        transaction
        for transaction in transactions
        if (
            isinstance(transaction.get("Описание"), str)
            and re.search(search_str, transaction["Описание"], re.IGNORECASE)
        )
        or (
            isinstance(transaction.get("Категория"), str)
            and re.search(search_str, transaction["Категория"], re.IGNORECASE)
        )
    ]
    except Exception as e:
        services_logger.error(f"Ошибка {e}")

    if not result:
        services_logger.info("Ничего не найдено")

    return json.dumps(result, sort_keys=False, indent=4, ensure_ascii=False)
