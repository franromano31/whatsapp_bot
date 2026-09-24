from datetime import date

from app.core.config import settings
from app.schemas.hotel import (
    AvailabilityRequest,
    AvailabilityResponse,
    RoomOption,
    ReservationRequest,
    ReservationResponse,
)


class HotelService:

    def __init__(self):
        self.base_url = settings.hotel_api_url
        self.token = settings.hotel_api_token
        self.mode = settings.hotel_api_mode

    async def test_connection(self):
        return {
            "mode": self.mode,
            "base_url": self.base_url,
            "configured": self.mode == "mock"
            or bool(self.base_url and self.token)
        }

    async def check_availability(
        self,
        request: AvailabilityRequest
    ) -> AvailabilityResponse:

        if self.mode == "mock":
            return self._mock_availability(request)

        raise NotImplementedError(
            "La conexión con la API real todavía no está implementada."
        )

    async def create_reservation(
    self,
        request: ReservationRequest
    ) -> ReservationResponse:

        if self.mode == "mock":
            return self._mock_create_reservation(request)

        raise NotImplementedError(
            "La creación de reservas en la API real todavía no está implementada."
        )

    def _mock_availability(
        self,
        request: AvailabilityRequest
    ) -> AvailabilityResponse:

        nights = (request.check_out - request.check_in).days

        price_per_night = 120000

        option = RoomOption(
            room_id=14,
            room_type="Doble Superior",
            capacity=2,
            meal_plan=request.meal_plan,
            price_per_night=price_per_night,
            total_price=price_per_night * nights,
            currency="ARS"
        )

        return AvailabilityResponse(
            available=True,
            check_in=request.check_in,
            check_out=request.check_out,
            guests=request.guests,
            options=[option]
        )

    def _mock_create_reservation(
        self,
        request: ReservationRequest
    ) -> ReservationResponse:

        nights = (request.check_out - request.check_in).days

        price_per_night = 120000
        total_price = price_per_night * nights

        return ReservationResponse(
            reservation_id=92831,
            code="RES-92831",
            status="pending_payment",
            room_id=request.room_id,
            check_in=request.check_in,
            check_out=request.check_out,
            total_price=total_price,
            currency="ARS"
        )


hotel_service = HotelService()