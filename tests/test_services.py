import json
from unittest.mock import patch

from src.services import services_simple_search
from tests.conftest import testing_transactions


def test_services_simple_search(testing_transactions):
    with patch("src.services.open_excel") as mock_file:
        mock_file.return_value = testing_transactions
        result_json = services_simple_search("топливо")
        result = json.loads(result_json)

        assert len(result) == 1
        assert "топливо" in result[0]["Категория"].lower()