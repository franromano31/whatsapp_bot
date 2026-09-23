import httpx

from app.core.config import settings


class HotelService:

    def __init__(self):
        self.base_url = settings.hotel_api_url
        self.token = settings.hotel_api_token

    async def test_connection(self):
        return {
            "base_url": self.base_url,
            "configured": bool(self.base_url and self.token)
        }


hotel_service = HotelService()