"""https://towardsdatascience.com/pydantic-or-dataclasses-why-not-both-convert-between-them-ba382f0f9a9c"""

from dataclasses import fields, MISSING, dataclass
from typing import Any, Optional

import pydantic

from src.domains import (EventId, EntityId)


def convert_flat_dataclass_to_pydantic(
        dcls: type, name: Optional[str] = None
) -> type[pydantic.BaseModel]:
    if name is None:
        name_ = f"Pydantic{dcls.__name__}"
    else:
        name_ = name
    return pydantic.create_model(  # type: ignore
        name_,
        **_get_pydantic_field_kwargs(dcls),
    )


def _get_pydantic_field_kwargs(dcls: dataclass) -> dict[str, tuple[type, Any]]:
    # get attribute names and types from dataclass into pydantic format
    pydantic_field_kwargs = dict()
    for _field in fields(dcls):
        # check is field has default value
        if isinstance(_field.default, type(MISSING)):
            # no default
            default = ...
        else:
            default = _field.default

        field_type = _field.type
        if field_type in {EventId, EntityId}:
            field_type = str

        pydantic_field_kwargs[_field.name] = (field_type, default)
    return pydantic_field_kwargs
