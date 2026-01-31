import unittest
from typing import Optional
from unittest.mock import Mock, patch

import requests

from src.mfapi.client import MFAPIClient
from src.mfapi.model import (
    LatestNAVItem,
    NAVHistoryResponse,
    SchemeListItem,
    SchemeSearchResult,
)


def make_mock_response(json_data, raise_exc: Optional[Exception] = None):
    """
    Helper to create a mock response object that mimics `requests.Response`
    for the purposes of these unit tests.
    """
    mock_resp = Mock()
    mock_resp.json = Mock(return_value=json_data)
    if raise_exc is None:
        mock_resp.raise_for_status = Mock()
    else:
        mock_resp.raise_for_status = Mock(side_effect=raise_exc)
    return mock_resp


class TestMFAPIClient(unittest.TestCase):
    def setUp(self):
        self.client = MFAPIClient()

    @patch("src.mfapi.client.requests.get")
    def test_search_schemes_success(self, mock_get):
        # Arrange
        payload = [{"schemeCode": 123, "schemeName": "Test Scheme"}]
        mock_get.return_value = make_mock_response(payload)

        # Act
        result = self.client.search_schemes("test")

        # Assert
        mock_get.assert_called_once_with(
            f"{self.client.BASE_URL}/mf/search", params={"q": "test"}
        )
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        item = result[0]
        self.assertIsInstance(item, SchemeSearchResult)
        self.assertEqual(item.scheme_code, 123)
        self.assertEqual(item.scheme_name, "Test Scheme")

    @patch("src.mfapi.client.requests.get")
    def test_list_schemes_success(self, mock_get):
        # Arrange
        payload = [
            {
                "schemeCode": 1,
                "schemeName": "Alpha Fund",
                "isinGrowth": "INE000A0001",
                "isinDivReinvestment": None,
            }
        ]
        mock_get.return_value = make_mock_response(payload)

        # Act
        result = self.client.list_schemes(limit=10, offset=0)

        # Assert
        mock_get.assert_called_once_with(
            f"{self.client.BASE_URL}/mf", params={"limit": 10, "offset": 0}
        )
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        item = result[0]
        self.assertIsInstance(item, SchemeListItem)
        self.assertEqual(item.scheme_code, 1)
        self.assertEqual(item.scheme_name, "Alpha Fund")
        self.assertEqual(item.isin_growth, "INE000A0001")
        self.assertIsNone(item.isin_div_reinvestment)

    @patch("src.mfapi.client.requests.get")
    def test_list_schemes_with_latest_nav_success(self, mock_get):
        # Arrange
        payload = [
            {
                "schemeCode": 200,
                "schemeName": "Beta Fund",
                "fundHouse": "Beta MF",
                "schemeType": "Open Ended Schemes",
                "schemeCategory": "Equity",
                "isinGrowth": None,
                "isinDivReinvestment": None,
                "nav": "1234.56789",
                "date": "01-01-2025",
            }
        ]
        mock_get.return_value = make_mock_response(payload)

        # Act
        result = self.client.list_schemes_with_latest_nav(limit=5, offset=2)

        # Assert
        mock_get.assert_called_once_with(
            f"{self.client.BASE_URL}/mf/latest", params={"limit": 5, "offset": 2}
        )
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        item = result[0]
        self.assertIsInstance(item, LatestNAVItem)
        self.assertEqual(item.scheme_code, 200)
        self.assertEqual(item.scheme_name, "Beta Fund")
        self.assertEqual(item.fund_house, "Beta MF")
        self.assertEqual(item.nav, "1234.56789")
        self.assertEqual(item.date, "01-01-2025")

    @patch("src.mfapi.client.requests.get")
    def test_get_nav_data_success(self, mock_get):
        # Arrange
        scheme_code = "1001"
        start_date = "01-01-2020"
        end_date = "31-01-2020"
        payload = {
            "meta": {
                "fund_house": "Gamma MF",
                "scheme_type": "Open Ended Schemes",
                "scheme_category": "Debt",
                "scheme_code": 1001,
                "scheme_name": "Gamma Fund",
                "isin_growth": None,
                "isin_div_reinvestment": None,
            },
            "data": [
                {"date": "01-01-2020", "nav": "10.00000"},
                {"date": "02-01-2020", "nav": "10.05000"},
            ],
            "status": "SUCCESS",
        }
        mock_get.return_value = make_mock_response(payload)

        # Act
        result = self.client.get_nav_data(scheme_code, start_date, end_date)

        # Assert
        mock_get.assert_called_once_with(
            f"{self.client.BASE_URL}/mf/{scheme_code}",
            params={"from": start_date, "to": end_date},
        )
        self.assertIsInstance(result, NAVHistoryResponse)
        self.assertEqual(result.status, "SUCCESS")
        self.assertEqual(result.meta.scheme_code, 1001)
        self.assertEqual(result.meta.scheme_name, "Gamma Fund")
        self.assertEqual(len(result.data), 2)
        self.assertEqual(result.data[0].date, "01-01-2020")
        self.assertEqual(result.data[0].nav, "10.00000")

    @patch("src.mfapi.client.requests.get")
    def test_get_latest_nav_success(self, mock_get):
        # Arrange
        scheme_code = "1001"
        payload = {
            "meta": {
                "fund_house": "Gamma MF",
                "scheme_type": "Open Ended Schemes",
                "scheme_category": "Debt",
                "scheme_code": 1001,
                "scheme_name": "Gamma Fund",
                "isin_growth": None,
                "isin_div_reinvestment": None,
            },
            "data": [
                {"date": "31-01-2020", "nav": "10.50000"},
            ],
            "status": "SUCCESS",
        }
        mock_get.return_value = make_mock_response(payload)

        # Act
        result = self.client.get_latest_nav(scheme_code)

        # Assert
        mock_get.assert_called_once_with(
            f"{self.client.BASE_URL}/mf/{scheme_code}/latest"
        )
        self.assertIsInstance(result, NAVHistoryResponse)
        self.assertEqual(result.status, "SUCCESS")
        self.assertEqual(result.data[0].nav, "10.50000")

    @patch("src.mfapi.client.requests.get")
    def test_raise_for_status_propagates(self, mock_get):
        # Arrange: simulate HTTP error in raise_for_status
        http_err = requests.exceptions.HTTPError("Bad request")
        mock_get.return_value = make_mock_response([], raise_exc=http_err)

        # Act / Assert
        with self.assertRaises(requests.exceptions.HTTPError):
            self.client.search_schemes("should-fail")

        mock_get.assert_called_once_with(
            f"{self.client.BASE_URL}/mf/search", params={"q": "should-fail"}
        )


if __name__ == "__main__":
    unittest.main()
