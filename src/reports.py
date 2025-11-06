import datetime
import logging
import os
from functools import wraps
from typing import Any, Callable, Optional

import pandas as pd
from dateutil.relativedelta import relativedelta
from openpyxl import Workbook

reports_logger = logging.getLogger("reports_logger")
logger_file = os.path.join((os.path.dirname(os.path.dirname(__file__))), "data", "reports.log")
reports_handler = logging.FileHandler(logger_file, mode="w")
reports_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
reports_handler.setFormatter(reports_formatter)
reports_logger.addHandler(reports_handler)
reports_logger.setLevel(logging.DEBUG)


def excel_creator_default(func: Callable[..., pd.DataFrame]) -> Callable[..., str]:
    """Декоратор, который принимает функцию, возвращающую DataFrame,
    и автоматически создает Excel-файл `category_report.xlsx`"""

    def wrapper(*args, **kwargs) -> str:
        df = func(*args, **kwargs)
        if not isinstance(df, pd.DataFrame):
            reports_logger.error("Функция должна возвращать pandas.DataFrame")
            raise TypeError("Функция должна возвращать pandas.DataFrame")

        wb = Workbook()
        sheet = wb.active
        sheet.title = "Report"

        sheet.append(list(df.columns))

        for _, row in df.iterrows():
            sheet.append(row.tolist())

        for col in sheet.columns:
            max_length = 0
            column = col[0].column_letter
            for cell in col:
                cell_value = str(cell.value) if cell.value is not None else ""
                if len(cell_value) > max_length:
                    max_length = len(cell_value)
            adjusted_width = max_length + 2
            sheet.column_dimensions[column].width = adjusted_width

        for i in range(1, sheet.max_row + 1):
            sheet.row_dimensions[i].height = 18

        report_filename = os.path.join(
            (os.path.dirname(os.path.dirname(__file__))), "data", f"{func.__name__}_report.xlsx"
        )
        wb.save(report_filename)
        reports_logger.info(f"Создан excel_отчет {report_filename}")
        return report_filename  # Возвращаем путь к файлу

    return wrapper


def excel_creator_filename(filename: Optional[str] = None) -> Any:
    """Декоратор, который принимает функцию, возвращающую DataFrame, и имя файла
    и создает Excel-файл с указанным именем"""

    def decorator(func: Callable[..., pd.DataFrame]) -> Callable[..., str]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> str:
            df = func(*args, **kwargs)
            if not isinstance(df, pd.DataFrame):
                reports_logger.error("Функция должна возвращать pandas.DataFrame")
                raise TypeError("Функция должна возвращать pandas.DataFrame")

            wb = Workbook()
            sheet = wb.active
            sheet.title = "Report"

            sheet.append(list(df.columns))

            for _, row in df.iterrows():
                sheet.append(row.tolist())

            for col in sheet.columns:
                max_length = 0
                column = col[0].column_letter
                for cell in col:
                    cell_value = str(cell.value) if cell.value is not None else ""
                    if len(cell_value) > max_length:
                        max_length = len(cell_value)
                adjusted_width = max_length + 2
                sheet.column_dimensions[column].width = adjusted_width

            for i in range(1, sheet.max_row + 1):
                sheet.row_dimensions[i].height = 18

            report_filename = os.path.join((os.path.dirname(os.path.dirname(__file__))), "data", f"{filename}.xlsx")
            wb.save(report_filename)
            reports_logger.info(f"Создан excel_отчет {report_filename}")
            return report_filename  # Возвращаем путь к файлу

        return wrapper

    return decorator


def spending_by_category(transactions_df: pd.DataFrame, category: str, date: Optional[str] = None) -> (
        Optional)[pd.DataFrame]:
    """ Отбор транзакций по заданной категории за последние 3 месяца от указанной даты """
    reports_logger.info("Формирование временного периода для отчета")
    if date:
        end_date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    else:
        end_date = datetime.datetime.now()

    start_date = end_date - relativedelta(months=3)

    transactions_df["Дата_операции_dt"] = pd.to_datetime(transactions_df["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    reports_logger.info("Поиск по операциям")
    sorted_transactions = transactions_df.loc[
        (transactions_df["Категория"] == category)
        & (start_date <= transactions_df["Дата_операции_dt"])
        & (transactions_df["Дата_операции_dt"] <= end_date)
    ]
    reports_logger.info("Список операций в заданной категории сформирован")

    return sorted_transactions


def report_spending_by_category(df: pd.DataFrame) -> str | None:
    """ Преобразование DF в json строку """

    sorted_transactions_json = df.to_json(orient="records", force_ascii=False)
    return sorted_transactions_json