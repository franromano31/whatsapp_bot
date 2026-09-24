from datetime import date

from app.core.config import settings
from app.schemas.hotel import (
    AvailabilityRequest,
    AvailabilityResponse,
    RoomOption,
    ReservationRequest,
    ReservationResponse,
    CancelReservationResponse,
)

from app.exceptions.hotel_exp import (
    InsufficientCapacityError,
    ReservationAlreadyCancelledError,
    ReservationNotFoundError,
    RoomDisabledError,
    RoomNotFoundError,
    RoomUnavailableError, 
)


class HotelService:

    def __init__(self):
        self.base_url = settings.hotel_api_url
        self.token = settings.hotel_api_token
        self.mode = settings.hotel_api_mode

        # Base de datos ficticia de habitaciones
        self.mock_rooms = [
            {
                "room_id": 14,
                "room_type": "Doble Superior",
                "capacity": 2,
                "price_per_night": 120000,
                "enabled": True,
            },
            {
                "room_id": 15,
                "room_type": "Doble Standard",
                "capacity": 2,
                "price_per_night": 95000,
                "enabled": True,
            },
            {
                "room_id": 20,
                "room_type": "Triple Superior",
                "capacity": 3,
                "price_per_night": 150000,
                "enabled": True,
            },
            {
                "room_id": 25,
                "room_type": "Cuádruple Familiar",
                "capacity": 4,
                "price_per_night": 180000,
                "enabled": False,
            },
        ]

        # Reservas ficticias
        self.mock_reservations = []

        # Para generar IDs
        self.next_reservation_id = 1

    async def test_connection(self):
        return {
            "mode": self.mode,
            "base_url": self.base_url,
            "configured": (
                self.mode == "mock"
                or bool(self.base_url and self.token)
            ),
        }

    async def check_availability(
        self,
        request: AvailabilityRequest,
    ) -> AvailabilityResponse:

        if self.mode == "mock":
            return self._mock_availability(request)

        raise NotImplementedError(
            "La conexión con la API real todavía no está implementada."
        )

    async def create_reservation(
        self,
        request: ReservationRequest,
    ) -> ReservationResponse:

        if self.mode == "mock":
            return self._mock_create_reservation(request)

        raise NotImplementedError(
            "La creación de reservas en la API real todavía no está implementada."
        )

    def _mock_availability(
        self,
        request: AvailabilityRequest,
    ) -> AvailabilityResponse:

        nights = (request.check_out - request.check_in).days

        options = []

        for room in self.mock_rooms:

            # Habitación deshabilitada
            if not room["enabled"]:
                continue

            # No entran los huéspedes
            if room["capacity"] < request.guests:
                continue

            # Está ocupada en esas fechas
            if not self._is_room_available(
                room_id=room["room_id"],
                check_in=request.check_in,
                check_out=request.check_out,
            ):
                continue

            option = RoomOption(
                room_id=room["room_id"],
                room_type=room["room_type"],
                capacity=room["capacity"],
                meal_plan=request.meal_plan,
                price_per_night=room["price_per_night"],
                total_price=room["price_per_night"] * nights,
                currency="ARS",
            )

            options.append(option)

        return AvailabilityResponse(
            available=len(options) > 0,
            check_in=request.check_in,
            check_out=request.check_out,
            guests=request.guests,
            options=options,
        )

    def _mock_create_reservation(
        self,
        request: ReservationRequest,
    ) -> ReservationResponse:

        room = next(
            (
                room
                for room in self.mock_rooms
                if room["room_id"] == request.room_id
            ),
            None,
        )

        if room is None:
            raise RoomNotFoundError("La habitación no existe")

        if not room["enabled"]:
            raise RoomDisabledError("La habitación está deshabilitada")

        if room["capacity"] < request.guests:
            raise InsufficientCapacityError("La habitación no tiene capacidad suficiente")

        if not self._is_room_available(
            room_id=request.room_id,
            check_in=request.check_in,
            check_out=request.check_out,
        ):
            raise RoomUnavailableError(
                "La habitación no está disponible para esas fechas"
            )

        nights = (
            request.check_out - request.check_in
        ).days

        total_price = (
            room["price_per_night"] * nights
        )

        reservation_id = self.next_reservation_id
        self.next_reservation_id += 1

        code = f"RES-{reservation_id:05d}"

        reservation = {
            "reservation_id": reservation_id,
            "code": code,
            "status": "pending_payment",
            "room_id": request.room_id,
            "check_in": request.check_in,
            "check_out": request.check_out,
            "guests": request.guests,
            "meal_plan": request.meal_plan,
            "guest": request.guest,
            "total_price": total_price,
            "currency": "ARS",
        }

        self.mock_reservations.append(reservation)

        return ReservationResponse(
            reservation_id=reservation_id,
            code=code,
            status="pending_payment",
            room_id=request.room_id,
            check_in=request.check_in,
            check_out=request.check_out,
            total_price=total_price,
            currency="ARS",
        )

    def _is_room_available(
        self,
        room_id: int,
        check_in: date,
        check_out: date,
    ) -> bool:

        for reservation in self.mock_reservations:

            if reservation["room_id"] != room_id:
                continue

            if reservation["status"] == "cancelled":
                continue

            existing_check_in = reservation["check_in"]
            existing_check_out = reservation["check_out"]

            overlaps = (
                check_in < existing_check_out
                and check_out > existing_check_in
            )

            if overlaps:
                return False

        return True

    async def cancel_reservation(
        self,
        reservation_id: int,
    ) -> CancelReservationResponse:

        if self.mode == "mock":
            return self._mock_cancel_reservation(
                reservation_id
            )

        raise NotImplementedError(
            "La cancelación en la API real todavía no está implementada."
        )

    def _mock_cancel_reservation(
        self,
        reservation_id: int,
    ) -> CancelReservationResponse:

        reservation = next(
            (
                reservation
                for reservation in self.mock_reservations
                if reservation["reservation_id"]
                == reservation_id
            ),
            None,
        )

        if reservation is None:
            raise ReservationNotFoundError(
                "La reserva no existe"
            )

        if reservation["status"] == "cancelled":
            raise ReservationAlreadyCancelledError(
                "La reserva ya está cancelada"
            )

        reservation["status"] = "cancelled"

        return CancelReservationResponse(
            reservation_id=reservation["reservation_id"],
            code=reservation["code"],
            status=reservation["status"],
        )


hotel_service = HotelService()