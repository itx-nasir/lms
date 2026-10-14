from datetime import datetime, time
from typing import Optional

from sqlalchemy import case, func
from sqlalchemy.orm import Session, joinedload

from auth import get_password_hash
from models import (
    AdminUser, Panel, PanelOrder, PanelTest, Patient, Test, TestCategory,
    TestOrder, TestOrderItem,
)
from schemas import CategoryIn, OrderIn, PanelIn, PatientIn, TestIn


class InUseError(Exception):
    """Raised when deleting a record that existing orders still reference."""


# ── Admin users ──────────────────────────────────────────────────────────────
def get_admin_user(db: Session, username: str):
    return db.query(AdminUser).filter(AdminUser.username == username).first()


def create_admin_user(db: Session, username: str, password: str):
    admin = AdminUser(username=username, hashed_password=get_password_hash(password))
    db.add(admin)
    db.commit()
    return admin


# ── Patients ─────────────────────────────────────────────────────────────────
def get_patients(db: Session):
    return db.query(Patient).order_by(Patient.id.desc()).all()


def create_patient(db: Session, data: PatientIn):
    patient = Patient(**data.model_dump())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


def update_patient(db: Session, patient_id: int, data: PatientIn):
    patient = db.get(Patient, patient_id)
    if patient:
        for key, value in data.model_dump().items():
            setattr(patient, key, value)
        db.commit()
    return patient


def delete_patient(db: Session, patient_id: int):
    patient = db.get(Patient, patient_id)
    if not patient:
        return
    if patient.orders:
        raise InUseError(f"{patient.name} has {len(patient.orders)} order(s) and cannot be deleted.")
    db.delete(patient)
    db.commit()


# ── Test catalog ─────────────────────────────────────────────────────────────
def get_test_categories(db: Session):
    return db.query(TestCategory).order_by(TestCategory.name).all()


def create_test_category(db: Session, data: CategoryIn):
    db.add(TestCategory(**data.model_dump()))
    db.commit()


def get_standalone_tests(db: Session):
    """Tests that are not part of any panel, i.e. orderable individually."""
    linked_test_ids = db.query(PanelTest.test_id)
    return (
        db.query(Test)
        .options(joinedload(Test.category))
        .filter(~Test.id.in_(linked_test_ids))
        .order_by(Test.name)
        .all()
    )


def _set_test_panel(db: Session, test_id: int, panel_id: Optional[int]):
    """A test belongs to at most one panel: drop any existing link, then relink."""
    db.query(PanelTest).filter(PanelTest.test_id == test_id).delete()
    if panel_id:
        sequence = db.query(PanelTest).filter(PanelTest.panel_id == panel_id).count()
        db.add(PanelTest(panel_id=panel_id, test_id=test_id, sequence=sequence))


def create_test(db: Session, data: TestIn):
    test = Test(**data.model_dump(exclude={"panel_id"}))
    db.add(test)
    db.flush()
    _set_test_panel(db, test.id, data.panel_id)
    db.commit()


def update_test(db: Session, test_id: int, data: TestIn):
    test = db.get(Test, test_id)
    if test:
        for key, value in data.model_dump(exclude={"panel_id"}).items():
            setattr(test, key, value)
        current_panel_id = test.panel_links[0].panel_id if test.panel_links else None
        if current_panel_id != data.panel_id:
            _set_test_panel(db, test_id, data.panel_id)
        db.commit()


def delete_test(db: Session, test_id: int):
    test = db.get(Test, test_id)
    if not test:
        return
    if test.order_items:
        raise InUseError(f'"{test.name}" is used in existing orders and cannot be deleted.')
    db.delete(test)
    db.commit()


def get_panels(db: Session):
    return (
        db.query(Panel)
        .options(joinedload(Panel.panel_tests).joinedload(PanelTest.test).joinedload(Test.category))
        .order_by(Panel.name)
        .all()
    )


def create_panel(db: Session, data: PanelIn):
    db.add(Panel(**data.model_dump()))
    db.commit()


def update_panel(db: Session, panel_id: int, data: PanelIn):
    panel = db.get(Panel, panel_id)
    if panel:
        for key, value in data.model_dump().items():
            setattr(panel, key, value)
        db.commit()


def delete_panel(db: Session, panel_id: int):
    """Delete a panel. Its member tests are kept and become individual tests."""
    panel = db.get(Panel, panel_id)
    if not panel:
        return
    if panel.panel_orders:
        raise InUseError(f'"{panel.name}" is used in existing orders and cannot be deleted.')
    db.delete(panel)
    db.commit()


# ── Orders ───────────────────────────────────────────────────────────────────
def get_orders(db: Session, status: Optional[str] = None, limit: Optional[int] = None):
    query = db.query(TestOrder).options(joinedload(TestOrder.patient))
    if status:
        query = query.filter(TestOrder.status == status)
    return query.order_by(TestOrder.id.desc()).limit(limit).all()


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


def create_order(db: Session, data: OrderIn):
    panel_ids = list(dict.fromkeys(data.panel_ids))
    test_ids = list(dict.fromkeys(data.test_ids))

    panels = (
        db.query(Panel).options(joinedload(Panel.panel_tests).joinedload(PanelTest.test))
        .filter(Panel.id.in_(panel_ids)).all()
    ) if panel_ids else []
    tests = db.query(Test).filter(Test.id.in_(test_ids)).all() if test_ids else []

    order = TestOrder(
        patient_id=data.patient_id,
        total_amount=sum(p.price for p in panels) + sum(t.price for t in tests),
        referred_by=data.referred_by,
        sample_collected_at=data.sample_collected_at,
    )
    db.add(order)
    db.flush()

    for panel in panels:
        panel_order = PanelOrder(order_id=order.id, panel_id=panel.id, price=panel.price)
        db.add(panel_order)
        db.flush()
        for pt in panel.panel_tests:
            db.add(TestOrderItem(
                order_id=order.id, test_id=pt.test_id,
                unit_price=pt.test.price, panel_order_id=panel_order.id,
            ))

    for test in tests:
        db.add(TestOrderItem(order_id=order.id, test_id=test.id, unit_price=test.price))

    db.commit()
    return order


def save_results(db: Session, order: TestOrder, form) -> None:
    """Store result/notes fields named result_value_<item id> / result_notes_<item id>.
    Blank fields clear any previously stored value."""
    for item in order.items:
        value = form.get(f"result_value_{item.id}")
        if value is None:
            continue
        notes = form.get(f"result_notes_{item.id}") or ""
        item.result_value = value.strip() or None
        item.result_notes = notes.strip() or None
    db.commit()


def complete_order(db: Session, order: TestOrder) -> None:
    order.status = "completed"
    order.reported_at = order.reported_at or datetime.now()
    order.sample_collected_at = order.sample_collected_at or order.ordered_at
    db.commit()


def delete_order(db: Session, order: TestOrder) -> None:
    db.delete(order)  # cascades to items and panel_orders
    db.commit()


# ── Dashboard ────────────────────────────────────────────────────────────────
def get_dashboard_stats(db: Session):
    today_start = datetime.combine(datetime.now().date(), time.min)
    stats = db.query(
        func.count(case((TestOrder.ordered_at >= today_start, TestOrder.id))).label("today"),
        func.count(case((TestOrder.status == "pending", TestOrder.id))).label("pending"),
        func.count(case((TestOrder.status == "completed", TestOrder.id))).label("completed"),
    ).first()
    return {
        "total_patients": db.query(func.count(Patient.id)).scalar(),
        "today_orders": stats.today,
        "pending_orders": stats.pending,
        "completed_orders": stats.completed,
    }
