#!/usr/bin/env python3
"""
Script to insert Haematology & Coagulation test data into the LMS database.
This script will insert CBC/CP test parameters with their normal ranges.
"""

from sqlalchemy.orm import sessionmaker
from database import engine, SessionLocal
from models import TestCategory, Test
import sys

# Test data
HAEMATOLOGY_DATA = [
    {
        "category": "Haematology & Coagulation",
        "test_name": "CBC/CP",
        "parameter": "Haemoglobin",
        "normal_range": "M:14-18 g/dl; F:11.5-16.5 g/dl"
    },
    {
        "category": "Haematology & Coagulation",
        "test_name": "CBC/CP",
        "parameter": "Haematocrit",
        "normal_range": "M:40-54%; F:37-47%"
    },
    {
        "category": "Haematology & Coagulation",
        "test_name": "CBC/CP",
        "parameter": "RBC Count",
        "normal_range": "4.1-5.9 million/cumm"
    },
    {
        "category": "Haematology & Coagulation",
        "test_name": "CBC/CP",
        "parameter": "MCV",
        "normal_range": "Adults:80-100 fl; Neonates:95-125 fl"
    },
    {
        "category": "Haematology & Coagulation",
        "test_name": "CBC/CP",
        "parameter": "MCH",
        "normal_range": "Adults:27-34 pg; Neonates:30-42 pg"
    },
    {
        "category": "Haematology & Coagulation",
        "test_name": "CBC/CP",
        "parameter": "MCHC",
        "normal_range": "Adults:32-36 g/dl; Neonates:30-34 g/dl"
    },
    {
        "category": "Haematology & Coagulation",
        "test_name": "CBC/CP",
        "parameter": "RDW",
        "normal_range": "11.0-16.0%"
    },
    {
        "category": "Haematology & Coagulation",
        "test_name": "CBC/CP",
        "parameter": "WBC Count",
        "normal_range": "4,000-11,000 per cumm"
    },
    {
        "category": "Haematology & Coagulation",
        "test_name": "CBC/CP",
        "parameter": "Neutrophils",
        "normal_range": "40-75%"
    },
    {
        "category": "Haematology & Coagulation",
        "test_name": "CBC/CP",
        "parameter": "Lymphocytes",
        "normal_range": "20-45%"
    },
    {
        "category": "Haematology & Coagulation",
        "test_name": "CBC/CP",
        "parameter": "Eosinophils",
        "normal_range": "1-4%"
    },
    {
        "category": "Haematology & Coagulation",
        "test_name": "CBC/CP",
        "parameter": "Monocytes",
        "normal_range": "1-6%"
    },
    {
        "category": "Haematology & Coagulation",
        "test_name": "CBC/CP",
        "parameter": "Basophils",
        "normal_range": "0-1%"
    },
    {
        "category": "Haematology & Coagulation",
        "test_name": "CBC/CP",
        "parameter": "Platelets",
        "normal_range": "150,000-400,000 per cumm"
    }
]

def get_or_create_category(db, category_name):
    """Get existing category or create new one."""
    category = db.query(TestCategory).filter(TestCategory.name == category_name).first()
    if not category:
        category = TestCategory(name=category_name)
        db.add(category)
        db.commit()
        db.refresh(category)
        print(f"Created new category: {category_name}")
    else:
        print(f"Found existing category: {category_name}")
    return category

def create_test(db, category_id, test_name, parameter, normal_range, price=0.0):
    """Create a new test entry."""
    # Combine test name and parameter for the full test name
    full_test_name = f"{test_name} - {parameter}"
    
    # Check if test already exists
    existing_test = db.query(Test).filter(
        Test.name == full_test_name,
        Test.category_id == category_id
    ).first()
    
    if existing_test:
        print(f"Test already exists: {full_test_name}")
        return existing_test
    
    # Create new test
    new_test = Test(
        name=full_test_name,
        price=price,
        reference_range=normal_range,
        category_id=category_id
    )
    
    db.add(new_test)
    db.commit()
    db.refresh(new_test)
    print(f"Created new test: {full_test_name}")
    return new_test

def insert_haematology_data():
    """Main function to insert all haematology data."""
    db = SessionLocal()
    
    try:
        print("Starting haematology data insertion...")
        print("-" * 50)
        
        # Get or create the category
        category = get_or_create_category(db, "Haematology & Coagulation")
        
        # Insert each test
        inserted_count = 0
        for data in HAEMATOLOGY_DATA:
            test = create_test(
                db=db,
                category_id=category.id,
                test_name=data["test_name"],
                parameter=data["parameter"],
                normal_range=data["normal_range"],
                price=0.0  # You can modify this default price
            )
            if test:
                inserted_count += 1
        
        print("-" * 50)
        print(f"Data insertion completed!")
        print(f"Category: {category.name} (ID: {category.id})")
        print(f"Tests processed: {len(HAEMATOLOGY_DATA)}")
        print(f"New tests created: {inserted_count}")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        db.rollback()
        sys.exit(1)
    
    finally:
        db.close()

def list_inserted_data():
    """Function to verify the inserted data."""
    db = SessionLocal()
    
    try:
        print("\nVerifying inserted data:")
        print("=" * 60)
        
        category = db.query(TestCategory).filter(
            TestCategory.name == "Haematology & Coagulation"
        ).first()
        
        if category:
            tests = db.query(Test).filter(Test.category_id == category.id).all()
            
            print(f"Category: {category.name}")
            print(f"Total tests in category: {len(tests)}")
            print("-" * 60)
            
            for test in tests:
                print(f"ID: {test.id}")
                print(f"Name: {test.name}")
                print(f"Reference Range: {test.reference_range}")
                print(f"Price: ${test.price}")
                print("-" * 40)
        else:
            print("Category 'Haematology & Coagulation' not found!")
    
    except Exception as e:
        print(f"Error occurred while verifying data: {str(e)}")
    
    finally:
        db.close()

if __name__ == "__main__":
    print("Haematology Data Insertion Script")
    print("="*50)
    
    # Check if tables exist, if not create them
    try:
        from database import create_tables
        create_tables()
        print("Database tables ready.")
    except Exception as e:
        print(f"Error setting up database: {str(e)}")
        sys.exit(1)
    
    # Insert the data
    insert_haematology_data()
    
    # Verify the inserted data
    list_inserted_data()
    
    print("\nScript completed successfully!")