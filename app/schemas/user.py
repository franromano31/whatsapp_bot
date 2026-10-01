from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    phone: str
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None


class UserResponse(BaseModel):
    id: int
    phone: str
    first_name: str | None
    last_name: str | None
    email: EmailStr | None

    model_config = {
        "from_attributes": True
    }