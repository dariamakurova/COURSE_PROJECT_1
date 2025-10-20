import os
import pandas as pd
import logging



def open_excel(file: str) -> list[dict]:
    """ Получение данных из .xlsx файла"""
    if os.path.exists(file):
        try:
            transactions = pd.read_excel(file).to_dict(orient="records")
        except ValueError as e:
            print(f'Ошибка {e}')
            return []
    else:
        print(f"Файл {file} не найден")
        return []
    return transactions

if __name__ == "__main__":
    path = os.path.join((os.path.dirname(os.path.dirname(__file__))), "data", "operations.xlsx")
    print(open_excel(path))