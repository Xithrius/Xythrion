import json
from dataclasses import dataclass

from httpx import AsyncClient, Response


@dataclass
class InternalAPIResponse:
    status: int
    data: dict


class APIClient:
    def __init__(self, base_url: str) -> None:
        self.http_client = AsyncClient()
        self.base_url = base_url

    async def close(self) -> None:
        await self.http_client.aclose()

    def full_url(self, partial_endpoint: str) -> str:
        extra_path_sep = "/" if partial_endpoint[0] != "/" else ""

        return f"{self.base_url}{extra_path_sep}{partial_endpoint}"

    async def request(
        self, method: str, partial_endpoint: str, **kwargs
    ) -> InternalAPIResponse:
        r: Response = await self.http_client.request(
            method.upper(), self.full_url(partial_endpoint), **kwargs
        )

        return InternalAPIResponse(r.status_code, r.json())

    async def get(self, partial_endpoint: str, **kwargs) -> InternalAPIResponse:
        return await self.request("GET", partial_endpoint, **kwargs)

    async def post(self, partial_endpoint: str, **kwargs) -> InternalAPIResponse:
        return await self.request(
            "POST", partial_endpoint, data=json.dumps(kwargs["data"], default=str)
        )

    async def delete(self, partial_endpoint: str, **kwargs) -> InternalAPIResponse:
        return await self.request("DELETE", partial_endpoint, **kwargs)
