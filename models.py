from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now)


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
    phone = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    orders = relationship("TestOrder", back_populates="patient")


class TestCategory(Base):
    __tablename__ = "test_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)

    tests = relationship("Test", back_populates="category")


class Test(Base):
    """A single lab parameter (e.g. "Haemoglobin"). May belong to at most one
    Panel via PanelTest; tests without a panel are ordered individually."""
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False, default=0.0)
    unit = Column(String(20), nullable=True)
    reference_range = Column(String(100), nullable=True)
    category_id = Column(Integer, ForeignKey("test_categories.id"), nullable=False)

    category = relationship("TestCategory", back_populates="tests")
    order_items = relationship("TestOrderItem", back_populates="test")
    panel_links = relationship("PanelTest", back_populates="test", cascade="all, delete-orphan")


class Panel(Base):
    """A named group of tests ordered together, e.g. "CBC/CP"."""
    __tablename__ = "panels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    price = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, default=datetime.now)

    panel_tests = relationship(
        "PanelTest", back_populates="panel",
        cascade="all, delete-orphan", order_by="PanelTest.sequence"
    )
    panel_orders = relationship("PanelOrder", back_populates="panel")

    @property
    def tests(self):
        return [pt.test for pt in self.panel_tests]

    @property
    def category(self):
        return self.panel_tests[0].test.category if self.panel_tests else None


class PanelTest(Base):
    __tablename__ = "panel_tests"

    id = Column(Integer, primary_key=True, index=True)
    panel_id = Column(Integer, ForeignKey("panels.id"), nullable=False)
    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False, unique=True)
    sequence = Column(Integer, default=0)

    panel = relationship("Panel", back_populates="panel_tests")
    test = relationship("Test", back_populates="panel_links")


class TestOrder(Base):
    __tablename__ = "test_orders"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    ordered_at = Column(DateTime, default=datetime.now)
    sample_collected_at = Column(DateTime, nullable=True)
    reported_at = Column(DateTime, nullable=True)
    total_amount = Column(Float, nullable=False, default=0.0)
    status = Column(String(20), nullable=False, default="pending")  # pending / completed
    referred_by = Column(String(150), nullable=True)

    patient = relationship("Patient", back_populates="orders")
    items = relationship("TestOrderItem", back_populates="order", cascade="all, delete-orphan")
    panel_orders = relationship("PanelOrder", back_populates="order", cascade="all, delete-orphan")
    share_links = relationship("ReportShareLink", back_populates="order", cascade="all, delete-orphan")


class PanelOrder(Base):
    """A whole Panel ordered as one line item, with its price frozen at order time."""
    __tablename__ = "panel_orders"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("test_orders.id"), nullable=False)
    panel_id = Column(Integer, ForeignKey("panels.id"), nullable=False)
    price = Column(Float, nullable=False)

    order = relationship("TestOrder", back_populates="panel_orders")
    panel = relationship("Panel", back_populates="panel_orders")
    items = relationship("TestOrderItem", back_populates="panel_order")


class TestOrderItem(Base):
    __tablename__ = "test_order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("test_orders.id"), nullable=False)
    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False)
    unit_price = Column(Float, nullable=False, default=0.0)  # frozen at order time
    result_value = Column(String(100), nullable=True)
    result_notes = Column(Text, nullable=True)
    panel_order_id = Column(Integer, ForeignKey("panel_orders.id"), nullable=True)

    order = relationship("TestOrder", back_populates="items")
    test = relationship("Test", back_populates="order_items")
    panel_order = relationship("PanelOrder", back_populates="items")


class ReportShareLink(Base):
    """An unguessable token that lets a patient open one report without logging in."""
    __tablename__ = "report_share_links"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("test_orders.id"), nullable=False)
    token = Column(String(64), unique=True, index=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    expires_at = Column(DateTime, nullable=False)

    order = relationship("TestOrder", back_populates="share_links")
