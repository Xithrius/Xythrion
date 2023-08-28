from httpx import AsyncClient, Response


class APIClient:
    def __init__(self, base_url: str) -> None:
        self.http_client = AsyncClient()
        self.base_url = base_url

    async def close(self) -> None:
        await self.http_client.aclose()

    def full_url(self, partial_endpoint: str) -> str:
        extra_path_sep = "/" if partial_endpoint[0] != "/" else ""

        return f"{self.base_url}{extra_path_sep}{partial_endpoint}"

    async def request(self, method: str, partial_endpoint: str, **kwargs) -> dict:
        r: Response = await self.http_client.request(
            method.upper(), self.full_url(partial_endpoint), **kwargs
        )

        r.raise_for_status()

        return r.json()

    async def get(self, partial_endpoint: str, **kwargs) -> dict:
        return await self.request("GET", partial_endpoint, **kwargs)

    async def post(self, partial_endpoint: str, **kwargs) -> dict:
        return await self.request("POST", partial_endpoint, **kwargs)

    async def delete(self, partial_endpoint: str, **kwargs) -> dict:
        return await self.request("DELETE", partial_endpoint, **kwargs)
