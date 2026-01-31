from typing import List, Optional
from functools import cache

import requests

from src.mfapi.model import (
    LatestNAVItem,
    NAVHistoryResponse,
    SchemeListItem,
    SchemeSearchResult,
)


class MFAPIClient:
    BASE_URL = "https://api.mfapi.in"

    @cache
    def search_schemes(self, query: str) -> List[SchemeSearchResult]:
        endpoint = f"{self.BASE_URL}/mf/search"
        response = requests.get(endpoint, params={"q": query})
        response.raise_for_status()
        return [SchemeSearchResult.model_validate(item) for item in response.json()]

    def list_schemes(self, limit: int, offset: int) -> List[SchemeListItem]:
        endpoint = f"{self.BASE_URL}/mf"
        response = requests.get(endpoint, params={"limit": limit, "offset": offset})
        response.raise_for_status()
        return [SchemeListItem.model_validate(item) for item in response.json()]

    def list_schemes_with_latest_nav(
        self, limit: int, offset: int
    ) -> List[LatestNAVItem]:
        endpoint = f"{self.BASE_URL}/mf/latest"
        response = requests.get(endpoint, params={"limit": limit, "offset": offset})
        response.raise_for_status()
        return [LatestNAVItem.model_validate(item) for item in response.json()]

    @cache
    def get_nav_data(
        self,
        scheme_code: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> NAVHistoryResponse:
        endpoint = f"{self.BASE_URL}/mf/{scheme_code}"
        response = requests.get(endpoint, params={"from": start_date, "to": end_date})
        response.raise_for_status()
        return NAVHistoryResponse.model_validate(response.json())

    @cache
    def get_latest_nav(self, scheme_code: str) -> NAVHistoryResponse:
        endpoint = f"{self.BASE_URL}/mf/{scheme_code}/latest"
        response = requests.get(endpoint)
        response.raise_for_status()
        return NAVHistoryResponse.model_validate(response.json())
