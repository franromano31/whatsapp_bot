from fastapi import FastAPI

from app.services.hotel_service import hotel_service
from fastapi import FastAPI, HTTPException

from app.core.database import test_database_connection, Base, engine
from app.models.user import User
from sqlalchemy import inspect


from app.schemas.user import (
    UserCreate,
    UserResponse,
)

from app.services.user_service import user_service

from app.schemas.hotel import (
    AvailabilityRequest,
    AvailabilityResponse,
    ReservationRequest,
    ReservationResponse,
    CancelReservationResponse,
)

from app.exceptions.hotel_exp import (
    RoomNotFoundError,
    RoomUnavailableError,
    RoomDisabledError,
    ReservationAlreadyCancelledError,
    ReservationNotFoundError,
    InsufficientCapacityError,
)

from app.exceptions.user_exp import UserAlreadyExistsError


app = FastAPI(
    title="Hotel WhatsApp Bot API",
    version="0.1.0"
)

Base.metadata.create_all(bind=engine)


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
    response_model=ReservationResponse,
)
async def create_reservation(
    request: ReservationRequest,
):
    try:
        return await hotel_service.create_reservation(
            request
        )

    except RoomNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except (
        RoomUnavailableError,
        RoomDisabledError,
        InsufficientCapacityError,
    ) as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        )


@app.post(
    "/hotel/reservations/{reservation_id}/cancel",
    response_model=CancelReservationResponse,
)
async def cancel_reservation(
    reservation_id: int,
):
    try:
        return await hotel_service.cancel_reservation(
            reservation_id
        )

    except ReservationNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except ReservationAlreadyCancelledError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        )

@app.get("/db/test")
def test_database():
    result = test_database_connection()

    return {
        "database": "connected",
        "result": result,
    }

@app.get("/db/tables")
def get_database_tables():
    inspector = inspect(engine)

    return {
        "tables": inspector.get_table_names()
    }

@app.post(
    "/users",
    response_model=UserResponse,
)
def create_user(request: UserCreate):

    try:
        return user_service.create_user(request)

    except UserAlreadyExistsError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        )


@app.get(
    "/users/by-phone/{phone}",
    response_model=UserResponse | None,
)
def get_user_by_phone(phone: str):
    return user_service.get_user_by_phone(phone)

@app.post(
    "/users/resolve/{phone}",
    response_model=UserResponse,
)
def resolve_user(phone: str):
    return user_service.get_or_create_user(phone)