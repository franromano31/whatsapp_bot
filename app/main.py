from fastapi import FastAPI

from app.services.hotel_service import hotel_service

from app.schemas.hotel import (
    AvailabilityRequest,
    AvailabilityResponse,
    ReservationRequest,
    ReservationResponse,
)


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


@app.post(
    "/hotel/availability",
    response_model=AvailabilityResponse
)
async def hotel_availability(
    request: AvailabilityRequest
):
    return await hotel_service.check_availability(request)

@app.post(
    "/hotel/reservations",
    response_model=ReservationResponse
)
async def create_reservation(
    request: ReservationRequest
):
    return await hotel_service.create_reservation(request)