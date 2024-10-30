# generated by datamodel-codegen:
#   filename:  medium_grade_workshop_month_general_production_indicators__models.yaml
#   timestamp: 2024-10-29T05:12:00+00:00

from __future__ import annotations

from typing import List, Optional

from msgspec import Meta, Struct
from typing_extensions import Annotated


class GeneralProductionIndicator(Struct):
    name: Optional[Annotated[str, Meta(description='Показатели')]] = None
    norm: Optional[Annotated[float, Meta(description='Норматив %')]] = None
    percentage_to_total: Optional[Annotated[float, Meta(description='%')]] = None
    percentage_to_total_for_period: Optional[
        Annotated[float, Meta(description='%')]
    ] = None
    total: Optional[Annotated[float, Meta(description='Всего т.')]] = None
    total_for_period: Optional[
        Annotated[float, Meta(description='Всего т. с начала периода')]
    ] = None


GeneralProductionIndicators = Annotated[
    List[GeneralProductionIndicator], Meta(description='Отчет по производству')
]


class MediumGradeWorkshopMonthGeneralProductionIndicatorsGetParametersQuery(Struct):
    start_date: str
    end_date: str


class MediumGradeWorkshopMonthGeneralProductionIndicatorsGetResponseItem(Struct):
    isTotal: Optional[bool] = None
    values: Optional[List[str]] = None


MediumGradeWorkshopMonthGeneralProductionIndicatorsGetResponse = List[
    MediumGradeWorkshopMonthGeneralProductionIndicatorsGetResponseItem
]