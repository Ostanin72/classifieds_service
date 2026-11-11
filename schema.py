from pydantic import BaseModel, ValidationError
from sqlalchemy import select
from db import User

from errors import HttpError


class CreateUser(BaseModel):
    username: str
    password: str
    email: str


class UpdateUser(BaseModel):
    username: str | None = None
    password: str | None = None
    email: str | None = None


def validate(
        json_data: dict,
        schema_cls: type[CreateUser | UpdateUser]
) -> dict:
    try:
        return schema_cls(**json_data).model_dump()
    except ValidationError as err:
        errors = err.errors
        for e in errors:
            e.pop('ctx', None)
        raise HttpError(errors, 404)


class CreatePosting(BaseModel):
    heading: str
    description: str
    owner_id: int


class UpdatePosting(BaseModel):
    heading: str | None = None
    description: str | None = None
    owner_id: int


def validate_posting(
        json_data: dict,
        schema_cls: type[CreatePosting | UpdatePosting],
        session
) -> dict:
    try:
        validated_data = schema_cls(**json_data).model_dump()
        print(validated_data)
    except ValidationError as err:
        errors = err.errors()
        for e in errors:
            e.pop('ctx', None)
        raise HttpError(errors, 422)

    owner_id = validated_data.get('owner_id')

    user_exists = (session.execute(select(User.id).where(User.id == owner_id))
                   .scalar_one_or_none())
    if not user_exists:
        raise HttpError('Пользователь не найден', 404)

    # 3. Если всё хорошо, возвращаем данные
    return validated_data
