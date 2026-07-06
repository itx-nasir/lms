from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Text, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
    phone = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    orders = relationship("TestOrder", back_populates="patient")

class TestCategory(Base):
    __tablename__ = "test_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)

    # Relationships
    tests = relationship("Test", back_populates="category")

class Test(Base):
    """A single lab parameter/test (e.g. "Haemoglobin"). May optionally
    belong to one Panel (e.g. "CBC/CP") via PanelTest, so that it can be
    ordered either on its own or bundled together with the rest of its panel."""
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False, default=0.0)
    unit = Column(String(20), nullable=True)
    reference_range = Column(String(100), nullable=True)
    category_id = Column(Integer, ForeignKey("test_categories.id"), nullable=False)

    # Relationships
    category = relationship("TestCategory", back_populates="tests")
    order_items = relationship("TestOrderItem", back_populates="test")
    panel_links = relationship("PanelTest", back_populates="test", cascade="all, delete-orphan")

    @property
    def panel(self):
        """Convenience accessor: the single Panel this test belongs to, or None."""
        return self.panel_links[0].panel if self.panel_links else None

class Panel(Base):
    """A named group of tests that are almost always ordered together,
    e.g. "CBC/CP", "Liver Function Tests", "Lipid Profile". Selecting a
    panel automatically selects every test that belongs to it."""
    __tablename__ = "panels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    price = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
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
        return self.tests[0].category if self.tests else None

class PanelTest(Base):
    """Join table linking a Panel to its member Tests (with display order)."""
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
    ordered_at = Column(DateTime, default=datetime.utcnow)
    sample_collected_at = Column(DateTime, nullable=True)
    reported_at = Column(DateTime, nullable=True)
    total_amount = Column(Float, nullable=False, default=0.0)
    status = Column(String(20), nullable=False, default="pending")  # pending/completed
    referred_by = Column(String(150), nullable=True)

    # Relationships
    patient = relationship("Patient", back_populates="orders")
    items = relationship("TestOrderItem", back_populates="order", cascade="all, delete-orphan")
    panel_orders = relationship("PanelOrder", back_populates="order", cascade="all, delete-orphan")

class PanelOrder(Base):
    """Records that a whole Panel was ordered, freezing its price at order
    time. Its member TestOrderItems point back here via panel_order_id so
    results/reports can still be grouped and displayed by panel."""
    __tablename__ = "panel_orders"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("test_orders.id"), nullable=False)
    panel_id = Column(Integer, ForeignKey("panels.id"), nullable=False)
    price = Column(Float, nullable=False)  # frozen panel price at order time

    order = relationship("TestOrder", back_populates="panel_orders")
    panel = relationship("Panel", back_populates="panel_orders")
    items = relationship("TestOrderItem", back_populates="panel_order")

class TestOrderItem(Base):
    __tablename__ = "test_order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("test_orders.id"), nullable=False)
    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False)
    unit_price = Column(Float, nullable=False, default=0.0)  # frozen test price at order time
    result_value = Column(String(100), nullable=True)
    result_notes = Column(Text, nullable=True)
    panel_order_id = Column(Integer, ForeignKey("panel_orders.id"), nullable=True)

    # Relationships
    order = relationship("TestOrder", back_populates="items")
    test = relationship("Test", back_populates="order_items")
    panel_order = relationship("PanelOrder", back_populates="items")
