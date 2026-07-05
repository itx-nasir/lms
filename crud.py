from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, func, case
from models import (
    Patient, Test, TestCategory, TestOrder, TestOrderItem, AdminUser,
    Panel, PanelTest, PanelOrder,
)
from schemas import (
    PatientCreate, PatientUpdate, TestCreate, TestUpdate, TestCategoryCreate,
    TestOrderCreate, TestOrderItemUpdate, PanelCreate, PanelUpdate,
)
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
def get_patients(db: Session, skip: int = 0, limit: int = 500, search: str = None):
    query = db.query(Patient)
    if search:
        query = query.filter(or_(
            Patient.name.contains(search),
            Patient.phone.contains(search)
        ))
    return query.order_by(Patient.id.desc()).offset(skip).limit(limit).all()

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
        for key, value in patient_update.dict(exclude_unset=True).items():
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
    return db.query(TestCategory).order_by(TestCategory.name).all()

def create_test_category(db: Session, category: TestCategoryCreate):
    db_category = TestCategory(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# Test CRUD
def get_tests(db: Session, category_id: Optional[int] = None):
    query = db.query(Test).options(joinedload(Test.category), joinedload(Test.panel_links).joinedload(PanelTest.panel))
    if category_id:
        query = query.filter(Test.category_id == category_id)
    return query.order_by(Test.name).all()

def get_standalone_tests(db: Session):
    """Tests that are not part of any panel - orderable individually."""
    linked_test_ids = db.query(PanelTest.test_id)
    return (
        db.query(Test)
        .options(joinedload(Test.category))
        .filter(~Test.id.in_(linked_test_ids))
        .order_by(Test.name)
        .all()
    )

def get_test(db: Session, test_id: int):
    return db.query(Test).options(joinedload(Test.category), joinedload(Test.panel_links)).filter(Test.id == test_id).first()

def _set_test_panel(db: Session, test_id: int, panel_id: Optional[int]):
    """Ensure a test belongs to at most one panel - clear any existing link
    then (optionally) create the new one."""
    db.query(PanelTest).filter(PanelTest.test_id == test_id).delete()
    if panel_id:
        sequence = db.query(PanelTest).filter(PanelTest.panel_id == panel_id).count()
        db.add(PanelTest(panel_id=panel_id, test_id=test_id, sequence=sequence))

def create_test(db: Session, test: TestCreate):
    data = test.dict(exclude={"panel_id"})
    db_test = Test(**data)
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    if test.panel_id:
        _set_test_panel(db, db_test.id, test.panel_id)
        db.commit()
    return db_test

def update_test(db: Session, test_id: int, test_update: TestUpdate):
    db_test = db.query(Test).filter(Test.id == test_id).first()
    if db_test:
        data = test_update.dict(exclude_unset=True, exclude={"panel_id"})
        for key, value in data.items():
            setattr(db_test, key, value)
        db.commit()
        if "panel_id" in test_update.dict(exclude_unset=True):
            _set_test_panel(db, test_id, test_update.panel_id)
            db.commit()
        db.refresh(db_test)
    return db_test

def delete_test(db: Session, test_id: int):
    db_test = db.query(Test).filter(Test.id == test_id).first()
    if db_test:
        db.delete(db_test)
        db.commit()
    return db_test

# Panel CRUD
def get_panels(db: Session):
    return (
        db.query(Panel)
        .options(joinedload(Panel.panel_tests).joinedload(PanelTest.test).joinedload(Test.category))
        .order_by(Panel.name)
        .all()
    )

def get_panel(db: Session, panel_id: int):
    return (
        db.query(Panel)
        .options(joinedload(Panel.panel_tests).joinedload(PanelTest.test))
        .filter(Panel.id == panel_id)
        .first()
    )

def create_panel(db: Session, panel: PanelCreate):
    db_panel = Panel(**panel.dict())
    db.add(db_panel)
    db.commit()
    db.refresh(db_panel)
    return db_panel

def update_panel(db: Session, panel_id: int, panel_update: PanelUpdate):
    db_panel = db.query(Panel).filter(Panel.id == panel_id).first()
    if db_panel:
        for key, value in panel_update.dict(exclude_unset=True).items():
            setattr(db_panel, key, value)
        db.commit()
        db.refresh(db_panel)
    return db_panel

def delete_panel(db: Session, panel_id: int):
    """Delete a panel. Member tests are kept, just unlinked (become standalone)."""
    db_panel = db.query(Panel).filter(Panel.id == panel_id).first()
    if db_panel:
        db.delete(db_panel)
        db.commit()
    return db_panel

# Test Order CRUD
def get_orders(db: Session, skip: int = 0, limit: int = 500, status: Optional[str] = None):
    query = db.query(TestOrder).options(joinedload(TestOrder.patient))
    if status:
        query = query.filter(TestOrder.status == status)
    return query.order_by(TestOrder.id.desc()).offset(skip).limit(limit).all()

def get_order(db: Session, order_id: int):
    return (
        db.query(TestOrder)
        .options(
            joinedload(TestOrder.patient),
            joinedload(TestOrder.items).joinedload(TestOrderItem.test).joinedload(Test.category),
            joinedload(TestOrder.items).joinedload(TestOrderItem.panel_order).joinedload(PanelOrder.panel),
        )
        .filter(TestOrder.id == order_id)
        .first()
    )

def create_order(db: Session, order: TestOrderCreate):
    panel_ids = list(dict.fromkeys(order.panel_ids or []))
    test_ids = list(dict.fromkeys(order.test_ids or []))

    panels = db.query(Panel).options(
        joinedload(Panel.panel_tests).joinedload(PanelTest.test)
    ).filter(Panel.id.in_(panel_ids)).all() if panel_ids else []

    standalone_tests = db.query(Test).filter(Test.id.in_(test_ids)).all() if test_ids else []

    total_amount = sum(p.price for p in panels) + sum(t.price for t in standalone_tests)

    db_order = TestOrder(
        patient_id=order.patient_id,
        total_amount=total_amount,
        status=order.status,
        referred_by=order.referred_by,
    )
    db.add(db_order)
    db.flush()  # get order.id

    for panel in panels:
        panel_order = PanelOrder(order_id=db_order.id, panel_id=panel.id, price=panel.price)
        db.add(panel_order)
        db.flush()  # get panel_order.id
        for pt in panel.panel_tests:
            db.add(TestOrderItem(
                order_id=db_order.id,
                test_id=pt.test_id,
                unit_price=pt.test.price,
                panel_order_id=panel_order.id,
            ))

    for test in standalone_tests:
        db.add(TestOrderItem(
            order_id=db_order.id,
            test_id=test.id,
            unit_price=test.price,
            panel_order_id=None,
        ))

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

def delete_order(db: Session, order_id: int):
    db_order = db.query(TestOrder).filter(TestOrder.id == order_id).first()
    if db_order:
        db.delete(db_order)  # cascades to items + panel_orders
        db.commit()
    return True

def group_order_items(order):
    """Group an order's line items by the panel they were ordered as part
    of (e.g. all CBC/CP parameters together), with any individually-ordered
    tests collected into a final "Other Tests" group. Used to render
    order/report pages in a clean, grouped way instead of one long list."""
    groups = []
    panel_groups = {}
    other_items = []

    for item in order.items:
        if item.panel_order_id:
            group = panel_groups.get(item.panel_order_id)
            if not group:
                group = {"label": item.panel_order.panel.name, "items": []}
                panel_groups[item.panel_order_id] = group
                groups.append(group)
            group["items"].append(item)
        else:
            other_items.append(item)

    if other_items:
        groups.append({"label": "Other Tests", "items": other_items})

    return groups

# Dashboard stats
def get_dashboard_stats(db: Session):
    total_patients = db.query(func.count(Patient.id)).scalar()

    order_stats = db.query(
        func.count(TestOrder.id).label("total"),
        func.count(case((TestOrder.status == "pending", TestOrder.id))).label("pending"),
        func.count(case((TestOrder.status == "completed", TestOrder.id))).label("completed"),
    ).first()

    return {
        "total_patients": total_patients,
        "total_orders": order_stats.total,
        "pending_orders": order_stats.pending,
        "completed_orders": order_stats.completed,
    }
