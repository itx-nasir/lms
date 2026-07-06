from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Auth schemas
class AdminUserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Patient schemas
class PatientBase(BaseModel):
    name: str
    age: int
    gender: str
    phone: str

PatientCreate = PatientBase

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    phone: Optional[str] = None

class Patient(PatientBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Test Category schemas
class TestCategoryBase(BaseModel):
    name: str

TestCategoryCreate = TestCategoryBase

class TestCategory(TestCategoryBase):
    id: int

    class Config:
        from_attributes = True

# Test schemas
class TestBase(BaseModel):
    name: str
    price: float = 0.0
    unit: Optional[str] = None
    reference_range: Optional[str] = None
    category_id: int
    panel_id: Optional[int] = None  # optional panel this test belongs to

TestCreate = TestBase

class TestUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    unit: Optional[str] = None
    reference_range: Optional[str] = None
    category_id: Optional[int] = None
    panel_id: Optional[int] = None

class Test(BaseModel):
    id: int
    name: str
    price: float
    unit: Optional[str] = None
    reference_range: Optional[str] = None
    category_id: int
    category: TestCategory

    class Config:
        from_attributes = True

# Panel schemas
class PanelBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = 0.0

class PanelCreate(PanelBase):
    pass

class PanelUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None

class Panel(PanelBase):
    id: int

    class Config:
        from_attributes = True

# Test Order schemas
class TestOrderItemBase(BaseModel):
    test_id: int
    result_value: Optional[str] = None
    result_notes: Optional[str] = None

TestOrderItemCreate = TestOrderItemBase

class TestOrderItemUpdate(BaseModel):
    result_value: Optional[str] = None
    result_notes: Optional[str] = None

class TestOrderItem(TestOrderItemBase):
    id: int
    unit_price: float
    panel_order_id: Optional[int] = None
    test: Test

    class Config:
        from_attributes = True

class TestOrderBase(BaseModel):
    patient_id: int
    status: str = "pending"
    referred_by: Optional[str] = None
    sample_collected_at: Optional[datetime] = None

class TestOrderCreate(TestOrderBase):
    test_ids: List[int] = []
    panel_ids: List[int] = []

class TestOrderUpdate(BaseModel):
    status: Optional[str] = None
    sample_collected_at: Optional[datetime] = None
    reported_at: Optional[datetime] = None

class TestOrder(TestOrderBase):
    id: int
    ordered_at: datetime
    total_amount: float
    patient: Patient
    items: List[TestOrderItem]

    class Config:
        from_attributes = True
