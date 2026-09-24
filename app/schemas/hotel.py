from datetime import date

from pydantic import BaseModel


class AvailabilityRequest(BaseModel):
    check_in: date
    check_out: date
    guests: int
    meal_plan: str


class RoomOption(BaseModel):
    room_id: int
    room_type: str
    capacity: int
    meal_plan: str
    price_per_night: float
    total_price: float
    currency: str


class AvailabilityResponse(BaseModel):
    available: bool
    check_in: date
    check_out: date
    guests: int
    options: list[RoomOption]

class GuestData(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str


class ReservationRequest(BaseModel):
    room_id: int
    check_in: date
    check_out: date
    guests: int
    meal_plan: str
    guest: GuestData


class ReservationResponse(BaseModel):
    reservation_id: int
    code: str
    status: str
    room_id: int
    check_in: date
    check_out: date
    total_price: float
    currency: str