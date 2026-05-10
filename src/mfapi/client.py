from typing import Any, List, Optional

import requests

from src.mfapi.model import (
    LatestNAVItem,
    NAVHistoryResponse,
    SchemeListItem,
    SchemeSearchResult,
)


class MFAPIClient:
    BASE_URL = "https://api.mfapi.in"
    DEFAULT_TIMEOUT = 10

    def __init__(self, timeout: float = DEFAULT_TIMEOUT) -> None:
        self.timeout = timeout

    def _get(
        self, endpoint: str, params: dict[str, Any] | None = None
    ) -> requests.Response:
        filtered_params: dict[str, Any] | None = (
            {key: value for key, value in params.items() if value is not None}
            if params
            else None
        )
        if filtered_params == {}:
            filtered_params = None

        response = requests.get(endpoint, params=filtered_params, timeout=self.timeout)
        response.raise_for_status()
        return response

    def search_schemes(self, query: str) -> List[SchemeSearchResult]:
        endpoint = f"{self.BASE_URL}/mf/search"
        response = self._get(endpoint, params={"q": query})
        return [SchemeSearchResult.model_validate(item) for item in response.json()]

    def list_schemes(self, limit: int, offset: int) -> List[SchemeListItem]:
        endpoint = f"{self.BASE_URL}/mf"
        response = self._get(endpoint, params={"limit": limit, "offset": offset})
        return [SchemeListItem.model_validate(item) for item in response.json()]

    def list_schemes_with_latest_nav(
        self, limit: int, offset: int
    ) -> List[LatestNAVItem]:
        endpoint = f"{self.BASE_URL}/mf/latest"
        response = self._get(endpoint, params={"limit": limit, "offset": offset})
        return [LatestNAVItem.model_validate(item) for item in response.json()]

    def get_nav_data(
        self,
        scheme_code: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> NAVHistoryResponse:
        endpoint = f"{self.BASE_URL}/mf/{scheme_code}"
        response = self._get(endpoint, params={"from": start_date, "to": end_date})
        return NAVHistoryResponse.model_validate(response.json())

    def get_latest_nav(self, scheme_code: str) -> NAVHistoryResponse:
        endpoint = f"{self.BASE_URL}/mf/{scheme_code}/latest"
        response = self._get(endpoint)
        return NAVHistoryResponse.model_validate(response.json())
