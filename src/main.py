# запускаем программу по сбору данных
import os

from src.reports import excel_creator_default, excel_creator_filename, spending_by_category, report_spending_by_category
from src.services import services_simple_search
from src.utils import open_excel, transfer_into_dataframe
from src.views import views_main

transactions_file = transactions_xlsx = os.path.join(
    (os.path.dirname(os.path.dirname(__file__))), "data", "operations.xlsx"
)
transactions = open_excel(transactions_file)
transactions_df = transfer_into_dataframe(transactions)

# Главная веб-страница - указать дату date

date = "2021-08-10 00:00:00"
json_views_main = views_main(date)
print(json_views_main)

# Простой поиск - указать слово для поиска search
search = "красота"
json_services_simple_search = services_simple_search(search, transactions)
print(json_services_simple_search)

# Отчет по тратам по категории - указать категорию category
# Cохранит в EXCEL и вернет в формате JSON

category = "Фастфуд"

filename = ""

if filename:
    decorator = excel_creator_filename(filename)
else:
    decorator = excel_creator_default

get_report = decorator(spending_by_category)
report = get_report(transactions_df, category, date)

print(report) # выведет путь к созданному файлу

json_spending_by_category = report_spending_by_category(spending_by_category(transactions_df, category, date))
print(json_spending_by_category)