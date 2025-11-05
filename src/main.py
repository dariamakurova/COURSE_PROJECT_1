# запускаем программу по сбору данных
import os

from src.reports import spending_by_category, report_spending_by_category
from src.services import services_simple_search
from src.utils import transfer_into_dataframe, open_excel
from src.views import views_main

# Главная веб-страница - указать дату date

date = "2021-08-10 00:00:00"
print(views_main(date))

# Простой поиск - указать слово для поиска search
search = 'красота'
print(services_simple_search(search))

# Отчет по тратам по категории - указать категорию category

transactions_file = transactions_xlsx = os.path.join((os.path.dirname(os.path.dirname(__file__))), "data", "operations.xlsx")
transactions = open_excel(transactions_file)
transactions_df = transfer_into_dataframe(transactions)

category = "Фастфуд"
report = spending_by_category(transactions_df, category, date)
report_json = report_spending_by_category(report)

print(report_json)



