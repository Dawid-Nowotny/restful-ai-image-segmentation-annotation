from pydantic import BaseModel, field_validator, Field, model_validator
from fastapi import Form, HTTPException, Query, status

from dataclasses import dataclass
from typing import Optional, List

@dataclass
class ImageData:
    threshold: float = Form(ge=0.0, le=1.0)

class TagRequest(BaseModel):
    tag: str

class CommentRequest(BaseModel):
    super_tag: bool
    tags: List[TagRequest]

class ImageFilterParams(BaseModel):
    threshold_range: Optional[str] = Field(Query(None))
    tags: Optional[List[str]] = Field(Query(None))
    classes: Optional[List[str]] = Field(Query(None))

    @field_validator('threshold_range')
    def validate_threshold_range(cls, value: Optional[str]) -> Optional[List[float]]:
        if value is None:
            return None

        try:
            threshold_range_list = [float(x) for x in value.split(',')]
            if len(threshold_range_list) > 2:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Zakres może mieć maksymalnie 2 wartości')

            if not all(0.01 <= x <= 1.0 for x in threshold_range_list):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Wartości zakresu muszą mieścić się w przedziale od 0.01 do 1')

            if len(threshold_range_list) == 2 and threshold_range_list[0] >= threshold_range_list[1]:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Dolna granica zakresu musi być mniejsza niż górna granica')

        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Zakres musi być listą wartości zmiennoprzecinkowych rozdzielonych przecinkami')

        return threshold_range_list
    
    @model_validator(mode='after')
    def check_at_least_one_field(cls, values) -> None:
        if not any(getattr(values, field) is not None for field in ['threshold_range', 'tags', 'classes']):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Przynajmniej jedna z filtrów musi mieć wartość')