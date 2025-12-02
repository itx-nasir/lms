from sqlalchemy.orm import Session
from sqlalchemy import or_
from models import Patient, Test, TestCategory, TestOrder, TestOrderItem, AdminUser
from schemas import PatientCreate, PatientUpdate, TestCreate, TestUpdate, TestCategoryCreate, TestOrderCreate, TestOrderItemUpdate
from auth import get_password_hash
from typing import List, Optional

# Admin User CRUD
def create_admin_user(db: Session, username: str, password: str):
    hashed_password = get_password_hash(password)
    db_admin = AdminUser(username=username, hashed_password=hashed_password)
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

def get_admin_user(db: Session, username: str):
    return db.query(AdminUser).filter(AdminUser.username == username).first()

# Patient CRUD
def get_patients(db: Session, skip: int = 0, limit: int = 100, search: str = None):
    query = db.query(Patient)
    if search:
        query = query.filter(or_(
            Patient.name.contains(search),
            Patient.phone.contains(search)
        ))
    return query.offset(skip).limit(limit).all()

def get_patient(db: Session, patient_id: int):
    return db.query(Patient).filter(Patient.id == patient_id).first()

def create_patient(db: Session, patient: PatientCreate):
    db_patient = Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def update_patient(db: Session, patient_id: int, patient_update: PatientUpdate):
    db_patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if db_patient:
        for key, value in patient_update.dict().items():
            setattr(db_patient, key, value)
        db.commit()
        db.refresh(db_patient)
    return db_patient

def delete_patient(db: Session, patient_id: int):
    db_patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if db_patient:
        db.delete(db_patient)
        db.commit()
    return db_patient

# Test Category CRUD
def get_test_categories(db: Session):
    return db.query(TestCategory).all()

def create_test_category(db: Session, category: TestCategoryCreate):
    db_category = TestCategory(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# Test CRUD
def get_tests(db: Session, category_id: Optional[int] = None):
    query = db.query(Test)
    if category_id:
        query = query.filter(Test.category_id == category_id)
    return query.all()

def get_tests_by_category(db: Session, category_id: int):
    return db.query(Test).filter(Test.category_id == category_id).all()

def get_test(db: Session, test_id: int):
    return db.query(Test).filter(Test.id == test_id).first()

def create_test(db: Session, test: TestCreate):
    db_test = Test(**test.dict())
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    return db_test

def update_test(db: Session, test_id: int, test_update: TestUpdate):
    db_test = db.query(Test).filter(Test.id == test_id).first()
    if db_test:
        for key, value in test_update.dict().items():
            setattr(db_test, key, value)
        db.commit()
        db.refresh(db_test)
    return db_test

def delete_test(db: Session, test_id: int):
    db_test = db.query(Test).filter(Test.id == test_id).first()
    if db_test:
        db.delete(db_test)
        db.commit()
    return db_test

# Test Order CRUD
def get_orders(db: Session, skip: int = 0, limit: int = 100, status: Optional[str] = None):
    query = db.query(TestOrder)
    if status:
        query = query.filter(TestOrder.status == status)
    return query.offset(skip).limit(limit).all()

def get_order(db: Session, order_id: int):
    return db.query(TestOrder).filter(TestOrder.id == order_id).first()

def create_order(db: Session, order: TestOrderCreate):
    # Calculate total amount
    tests = db.query(Test).filter(Test.id.in_(order.test_ids)).all()
    total_amount = sum(test.price for test in tests)
    
    # Create order
    db_order = TestOrder(
        patient_id=order.patient_id,
        total_amount=total_amount,
        status=order.status
    )
    db.add(db_order)
    db.flush()  # Get the order ID
    
    # Create order items
    for test_id in order.test_ids:
        db_item = TestOrderItem(order_id=db_order.id, test_id=test_id)
        db.add(db_item)
    
    db.commit()
    db.refresh(db_order)
    return db_order

def update_order_status(db: Session, order_id: int, status: str):
    db_order = db.query(TestOrder).filter(TestOrder.id == order_id).first()
    if db_order:
        db_order.status = status
        db.commit()
        db.refresh(db_order)
    return db_order

def update_order_item_result(db: Session, item_id: int, result_update: TestOrderItemUpdate):
    db_item = db.query(TestOrderItem).filter(TestOrderItem.id == item_id).first()
    if db_item:
        if result_update.result_value is not None:
            db_item.result_value = result_update.result_value
        if result_update.result_notes is not None:
            db_item.result_notes = result_update.result_notes
        db.commit()
        db.refresh(db_item)
    return db_item

# Dashboard stats
def get_dashboard_stats(db: Session):
    total_patients = db.query(Patient).count()
    total_orders = db.query(TestOrder).count()
    pending_orders = db.query(TestOrder).filter(TestOrder.status == "pending").count()
    completed_orders = db.query(TestOrder).filter(TestOrder.status == "completed").count()
    
    return {
        "total_patients": total_patients,
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "completed_orders": completed_orders
    }