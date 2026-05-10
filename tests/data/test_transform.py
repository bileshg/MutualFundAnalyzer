import unittest
from datetime import date, timedelta

import pandas as pd

from src.data.transform import (
    NAV_ANALYSIS_COLUMNS,
    calculate_moving_average,
    process_nav_data,
)
from src.mfapi.model import NAVData


class TestNavTransforms(unittest.TestCase):
    def test_process_nav_data_empty_input_returns_stable_columns(self):
        result = process_nav_data([])

        self.assertTrue(result.empty)
        self.assertEqual(list(result.columns), NAV_ANALYSIS_COLUMNS)

    def test_process_nav_data_invalid_rows_returns_stable_columns(self):
        nav_data = [
            NAVData(date="not-a-date", nav="10.00000"),
            NAVData(date="01-01-2025", nav="not-a-number"),
        ]

        result = process_nav_data(nav_data)

        self.assertTrue(result.empty)
        self.assertEqual(list(result.columns), NAV_ANALYSIS_COLUMNS)

    def test_process_nav_data_includes_moving_average_columns(self):
        start_date = date(2025, 1, 1)
        nav_data = [
            NAVData(
                date=(start_date + timedelta(days=index)).strftime("%d-%m-%Y"),
                nav=str(index + 1),
            )
            for index in range(220)
        ]

        result = process_nav_data(nav_data)

        self.assertEqual(list(result.columns), NAV_ANALYSIS_COLUMNS)
        self.assertFalse(result.empty)
        self.assertTrue(result["50_DMA"].notna().any())
        self.assertTrue(result["200_DMA"].notna().any())

    def test_calculate_moving_average_rejects_invalid_windows(self):
        df = pd.DataFrame({"NAV": [1, 2, 3]})

        with self.assertRaises(ValueError):
            calculate_moving_average(df, 0)


if __name__ == "__main__":
    unittest.main()
