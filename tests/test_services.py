import json
from unittest.mock import patch

from src.services import services_simple_search


def test_services_simple_search(testing_transactions):

    result_json = services_simple_search("топливо", testing_transactions)
    result = json.loads(result_json)

    assert len(result) == 1
    assert "топливо" in result[0]["Категория"].lower()
