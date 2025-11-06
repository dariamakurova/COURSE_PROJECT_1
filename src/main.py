# запускаем программу по сбору данных
import os

from src.reports import spending_by_category, excel_creator_default, excel_creator_filename
from src.services import services_simple_search
from src.utils import open_excel, transfer_into_dataframe
from src.views import views_main

# Главная веб-страница - указать дату date

date = "2021-08-10 00:00:00"
print(views_main(date))

# Простой поиск - указать слово для поиска search
search = "красота"
print(services_simple_search(search))

# Отчет по тратам по категории - указать категорию category

transactions_file = transactions_xlsx = os.path.join(
    (os.path.dirname(os.path.dirname(__file__))), "data", "operations.xlsx"
)
transactions = open_excel(transactions_file)
transactions_df = transfer_into_dataframe(transactions)

category = "Фастфуд"

filename = ""

if filename:
    decorator = excel_creator_filename(filename)
else:
    decorator = excel_creator_default

get_report = decorator(spending_by_category)
report = get_report(transactions_df, category, date)

print(report)
