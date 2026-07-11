import aiohttp


class DaDataError(Exception):
    pass


class DaDataClient:
    FIND_BY_ID_URL = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/party"
    REQUEST_TIMEOUT = aiohttp.ClientTimeout(total=10)

    def __init__(self, api_key: str):
        self.api_key = api_key

    async def find_party(self, query: str) -> dict:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Token {self.api_key}",
        }
        try:
            async with aiohttp.ClientSession(timeout=self.REQUEST_TIMEOUT) as session:
                async with session.post(self.FIND_BY_ID_URL, json={"query": query}, headers=headers) as response:
                    body = await response.json()
                    if response.status != 200:
                        raise DaDataError(f"DaData returned {response.status}: {body}")
                    return body
        except aiohttp.ClientError as exc:
            raise DaDataError(str(exc)) from exc
