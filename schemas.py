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

class PatientCreate(PatientBase):
    pass

class PatientUpdate(PatientBase):
    pass

class Patient(PatientBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Test Category schemas
class TestCategoryBase(BaseModel):
    name: str

class TestCategoryCreate(TestCategoryBase):
    pass

class TestCategory(TestCategoryBase):
    id: int

    class Config:
        from_attributes = True

# Test schemas
class TestBase(BaseModel):
    name: str
    price: float
    unit: Optional[str] = None
    reference_range: Optional[str] = None
    category_id: int

class TestCreate(TestBase):
    pass

class TestUpdate(TestBase):
    pass

class Test(TestBase):
    id: int
    category: TestCategory

    class Config:
        from_attributes = True

# Test Order schemas
class TestOrderItemBase(BaseModel):
    test_id: int
    result_value: Optional[str] = None
    result_notes: Optional[str] = None

class TestOrderItemCreate(TestOrderItemBase):
    pass

class TestOrderItemUpdate(BaseModel):
    result_value: Optional[str] = None
    result_notes: Optional[str] = None

class TestOrderItem(TestOrderItemBase):
    id: int
    test: Test

    class Config:
        from_attributes = True

class TestOrderBase(BaseModel):
    patient_id: int
    status: str = "pending"

class TestOrderCreate(TestOrderBase):
    test_ids: List[int]

class TestOrderUpdate(BaseModel):
    status: Optional[str] = None

class TestOrder(TestOrderBase):
    id: int
    ordered_at: datetime
    total_amount: float
    patient: Patient
    items: List[TestOrderItem]

    class Config:
        from_attributes = True