from fastapi import FastAPI

from app.services.hotel_service import hotel_service


app = FastAPI(
    title="Hotel WhatsApp Bot API",
    version="0.1.0"
)


@app.get("/")
def home():
    return {
        "message": "Hotel WhatsApp Bot API funcionando"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.get("/hotel/test")
async def test_hotel():
    return await hotel_service.test_connection()