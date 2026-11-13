from pydantic import BaseModel, ValidationError

from errors import HttpError


class CreateUser(BaseModel):
    username: str
    password: str
    email: str


class UpdateUser(BaseModel):
    username: str | None = None
    password: str | None = None
    email: str | None = None


def validate(json_data: dict, schema_cls: type[CreateUser | UpdateUser]) -> dict:
    try:
        return schema_cls(**json_data).model_dump()
    except ValidationError as err:
        errors = err.errors()
        for e in errors:
            e.pop("ctx", None)
        raise HttpError(errors, 422)


class CreatePosting(BaseModel):
    heading: str
    description: str
    owner_id: int


class UpdatePosting(BaseModel):
    heading: str | None = None
    description: str | None = None


def validate_posting(
    json_data: dict, schema_cls: type[CreatePosting | UpdatePosting], session
) -> dict:
    try:
        return schema_cls(**json_data).model_dump()

    except ValidationError as err:
        errors = err.errors()
        for e in errors:
            e.pop("ctx", None)
        raise HttpError(errors, 422)
