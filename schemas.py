from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class PatientIn(BaseModel):
    name: str
    age: int
    gender: str
    phone: str


class CategoryIn(BaseModel):
    name: str


class TestIn(BaseModel):
    name: str
    price: float = 0.0
    unit: Optional[str] = None
    reference_range: Optional[str] = None
    category_id: int
    panel_id: Optional[int] = None


class PanelIn(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = 0.0


class OrderIn(BaseModel):
    patient_id: int
    referred_by: Optional[str] = None
    sample_collected_at: Optional[datetime] = None
    test_ids: List[int] = []
    panel_ids: List[int] = []
