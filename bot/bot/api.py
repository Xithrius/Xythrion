import json

from httpx import AsyncClient, Response


class APIClient:
    def __init__(self, base_url: str) -> None:
        self.http_client = AsyncClient(base_url=base_url)

    async def aclose(self) -> None:
        await self.http_client.aclose()

    async def request(self, method: str, partial_endpoint: str, **kwargs) -> Response:
        r: Response = await self.http_client.request(
            method.upper(),
            partial_endpoint,
            **kwargs,
        )

        return r

    async def get(self, partial_endpoint: str, **kwargs) -> Response:
        return await self.request(
            "GET",
            partial_endpoint,
            **kwargs,
        )

    async def post(self, partial_endpoint: str, **kwargs) -> Response:
        data = kwargs.pop("data")

        return await self.request(
            "POST",
            partial_endpoint,
            data=json.dumps(data, default=str),
            **kwargs,
        )

    async def put(self, partial_endpoint: str, **kwargs) -> Response:
        return await self.request(
            "PUT",
            partial_endpoint,
            **kwargs,
        )

    async def delete(self, partial_endpoint: str, **kwargs) -> Response:
        return await self.request(
            "DELETE",
            partial_endpoint,
            **kwargs,
        )
