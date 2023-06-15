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
    __tablename__ = "tests"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    unit = Column(String(20), nullable=True)
    reference_range = Column(String(100), nullable=True)
    category_id = Column(Integer, ForeignKey("test_categories.id"), nullable=False)
    
    # Relationships
    category = relationship("TestCategory", back_populates="tests")
    order_items = relationship("TestOrderItem", back_populates="test")

class TestOrder(Base):
    __tablename__ = "test_orders"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    ordered_at = Column(DateTime, default=datetime.utcnow)
    total_amount = Column(Float, nullable=False, default=0.0)
    status = Column(String(20), nullable=False, default="pending")  # pending/completed
    
    # Relationships
    patient = relationship("Patient", back_populates="orders")
    items = relationship("TestOrderItem", back_populates="order", cascade="all, delete-orphan")

class TestOrderItem(Base):
    __tablename__ = "test_order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("test_orders.id"), nullable=False)
    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False)
    result_value = Column(String(100), nullable=True)
    result_notes = Column(Text, nullable=True)
    
    # Relationships
    order = relationship("TestOrder", back_populates="items")
    test = relationship("Test", back_populates="order_items")