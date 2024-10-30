# generated by datamodel-codegen:
#   filename:  medium_grade_workshop_month_unfinished_rolling__models.yaml
#   timestamp: 2024-10-29T05:12:02+00:00

from __future__ import annotations

from typing import List, Optional

from msgspec import Meta, Struct
from typing_extensions import Annotated


class UnfinishedRollingItem(Struct):
    name: Optional[Annotated[str, Meta(description='Название строки')]] = None
    norm: Optional[Annotated[float, Meta(description='Норматив %')]] = None
    percentage_to_total: Optional[Annotated[float, Meta(description='%')]] = None
    percentage_to_total_for_period: Optional[
        Annotated[float, Meta(description='%')]
    ] = None
    total: Optional[Annotated[float, Meta(description='Всего т.')]] = None
    total_for_period: Optional[
        Annotated[float, Meta(description='Всего т. с начала периода')]
    ] = None


UnfinishedRolling = Annotated[
    List[UnfinishedRollingItem], Meta(description='Отчет по производству')
]


class MediumGradeWorkshopMonthUnfinishedRollingGetParametersQuery(Struct):
    start_date: str
    end_date: str


class MediumGradeWorkshopMonthUnfinishedRollingGetResponseItem(Struct):
    isTotal: Optional[bool] = None
    values: Optional[List[str]] = None


MediumGradeWorkshopMonthUnfinishedRollingGetResponse = List[
    MediumGradeWorkshopMonthUnfinishedRollingGetResponseItem
]