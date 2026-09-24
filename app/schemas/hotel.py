from datetime import date

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    model_validator,
)


class AvailabilityRequest(BaseModel):
    check_in: date
    check_out: date
    guests: int = Field(gt=0)
    meal_plan: str

    @model_validator(mode="after")
    def validate_dates(self):
        if self.check_out <= self.check_in:
            raise ValueError(
                "check_out debe ser posterior a check_in"
            )

        return self


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
    email: EmailStr
    phone: str


class ReservationRequest(BaseModel):
    room_id: int
    check_in: date
    check_out: date
    guests: int = Field(gt=0)
    meal_plan: str
    guest: GuestData

    @model_validator(mode="after")
    def validate_dates(self):
        if self.check_out <= self.check_in:
            raise ValueError(
                "check_out debe ser posterior a check_in"
            )

        return self

class ReservationResponse(BaseModel):
    reservation_id: int
    code: str
    status: str
    room_id: int
    check_in: date
    check_out: date
    total_price: float
    currency: str

class CancelReservationResponse(BaseModel):
    reservation_id: int
    code: str
    status: str