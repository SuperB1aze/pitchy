import aiohttp


class DaMiaError(Exception):
    pass


class DaMiaFsspClient:
    ISPS_URL = "https://api.damia.ru/fssp/isps"
    REQUEST_TIMEOUT = aiohttp.ClientTimeout(total=10)

    def __init__(self, api_key: str):
        self.api_key = api_key

    async def find_by_inn(self, inn: str) -> list[dict]:
        params = {"inn": inn, "format": "2", "key": self.api_key}
        try:
            async with aiohttp.ClientSession(timeout=self.REQUEST_TIMEOUT) as session:
                async with session.get(self.ISPS_URL, params=params) as response:
                    body = await response.json(content_type=None)
                    if response.status != 200:
                        raise DaMiaError(f"DaMIA returned {response.status}: {body}")
                    # DaMIA отправляет ошибки (неверный ключ, неверные параметры и т.д.) как HTTP 200 с пустым JSON-строковым телом вместо ожидаемого массива.
                    if isinstance(body, str):
                        raise DaMiaError(body)
                    if isinstance(body, dict) and body.get("error"):
                        raise DaMiaError(str(body["error"]))
                    return body if isinstance(body, list) else []
        except aiohttp.ClientError as exc:
            raise DaMiaError(str(exc)) from exc
