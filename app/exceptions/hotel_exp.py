class HotelError(Exception):
    pass


class RoomNotFoundError(HotelError):
    pass


class RoomUnavailableError(HotelError):
    pass


class RoomDisabledError(HotelError):
    pass


class InsufficientCapacityError(HotelError):
    pass


class ReservationNotFoundError(HotelError):
    pass


class ReservationAlreadyCancelledError(HotelError):
    pass