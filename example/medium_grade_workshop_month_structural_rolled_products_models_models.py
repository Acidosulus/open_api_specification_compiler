# generated by datamodel-codegen:
#   filename:  medium_grade_workshop_month_structural_rolled_products__models.yaml
#   timestamp: 2024-10-29T05:12:01+00:00

from __future__ import annotations

from typing import List, Optional

from msgspec import Meta, Struct
from typing_extensions import Annotated


class StructuralRolledProduct(Struct):
    accepted: Optional[Annotated[float, Meta(description='Принято, т')]] = None
    name: Optional[Annotated[str, Meta(description='Вид дефекта')]] = None
    percent: Optional[Annotated[float, Meta(description='%')]] = None
    total: Optional[Annotated[float, Meta(description='Всего, т')]] = None


StructuralRolledProducts = Annotated[
    List[StructuralRolledProduct], Meta(description='Конструкционный прокат')
]


class MediumGradeWorkshopMonthStructuralRolledProductsGetParametersQuery(Struct):
    start_date: str
    end_date: str


class MediumGradeWorkshopMonthStructuralRolledProductsGetResponseItem(Struct):
    isTotal: Optional[bool] = None
    values: Optional[List[str]] = None


MediumGradeWorkshopMonthStructuralRolledProductsGetResponse = List[
    MediumGradeWorkshopMonthStructuralRolledProductsGetResponseItem
]
