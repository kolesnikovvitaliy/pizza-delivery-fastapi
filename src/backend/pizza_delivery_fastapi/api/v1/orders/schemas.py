from typing import Annotated
from pydantic import BaseModel
from pydantic import ConfigDict, Field
from datetime import datetime
from sqlalchemy_utils.types.choice import Choice
from pydantic.functional_validators import AfterValidator


def convert_choice(choice: Choice) -> str:
    return str(choice)


class CustomOrderModel(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        from_attributes=True,
    )


class CreateOrder(CustomOrderModel):
    quantity: int
    pizza_size: str = Field(default="SMALL")


class ShowOrder(CustomOrderModel):
    id: int
    user_id: int
    pizza_size: Annotated[..., AfterValidator(convert_choice)] = Field(
        default="SMALL"
    )
    quantity: int
    order_status: Annotated[..., AfterValidator(convert_choice)] = Field(
        default="PENDING"
    )
    created_at: datetime


class OrderUpdate(CustomOrderModel):
    order_status: Annotated[..., AfterValidator(convert_choice)] = Field(
        default="PENDING"
    )


class OrderUpdatePartial(CustomOrderModel):
    pizza_size: Annotated[..., AfterValidator(convert_choice)] = Field(
        default="SMALL"
    )
    quantity: int
