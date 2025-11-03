import json
from unittest.mock import patch

from src.services import services_simple_search
from src.views import views_main


def test_views_main(testing_transactions):

    with patch("src.services.open_excel") as mock_file:
        mock_file.return_value = testing_transactions
        date = "2018-10-01 21:31:46"
        result_json = views_main(date)
        result = json.loads(result_json)

    assert result["greeting"] == "Добрый вечер"
