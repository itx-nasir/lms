#!/usr/bin/env python3
"""
Script to insert Urinalysis test data into the LMS database.
This script will insert comprehensive urinalysis test parameters with their normal ranges.
"""

from sqlalchemy.orm import sessionmaker
from database import engine, SessionLocal
from models import TestCategory, Test
import sys

# Urinalysis test data - typical clinical laboratory parameters
URINALYSIS_DATA = [
    # Physical Examination
    {
        "category": "Urinalysis",
        "test_name": "Physical Examination",
        "parameter": "Color",
        "normal_range": "Yellow to amber"
    },
    {
        "category": "Urinalysis",
        "test_name": "Physical Examination",
        "parameter": "Appearance",
        "normal_range": "Clear"
    },
    {
        "category": "Urinalysis",
        "test_name": "Physical Examination",
        "parameter": "Specific Gravity",
        "normal_range": "1.003-1.030"
    },
    {
        "category": "Urinalysis",
        "test_name": "Physical Examination",
        "parameter": "pH",
        "normal_range": "4.5-8.0"
    },
    
    # Chemical Examination
    {
        "category": "Urinalysis",
        "test_name": "Chemical Examination",
        "parameter": "Protein",
        "normal_range": "Negative or trace (<30 mg/dL)"
    },
    {
        "category": "Urinalysis",
        "test_name": "Chemical Examination",
        "parameter": "Glucose",
        "normal_range": "Negative (<15 mg/dL)"
    },
    {
        "category": "Urinalysis",
        "test_name": "Chemical Examination",
        "parameter": "Ketones",
        "normal_range": "Negative (<5 mg/dL)"
    },
    {
        "category": "Urinalysis",
        "test_name": "Chemical Examination",
        "parameter": "Blood",
        "normal_range": "Negative"
    },
    {
        "category": "Urinalysis",
        "test_name": "Chemical Examination",
        "parameter": "Bilirubin",
        "normal_range": "Negative (<0.2 mg/dL)"
    },
    {
        "category": "Urinalysis",
        "test_name": "Chemical Examination",
        "parameter": "Urobilinogen",
        "normal_range": "0.1-1.0 EU/dL"
    },
    {
        "category": "Urinalysis",
        "test_name": "Chemical Examination",
        "parameter": "Nitrites",
        "normal_range": "Negative"
    },
    {
        "category": "Urinalysis",
        "test_name": "Chemical Examination",
        "parameter": "Leukocyte Esterase",
        "normal_range": "Negative"
    },
    
    # Microscopic Examination
    {
        "category": "Urinalysis",
        "test_name": "Microscopic Examination",
        "parameter": "RBC",
        "normal_range": "0-2 per hpf"
    },
    {
        "category": "Urinalysis",
        "test_name": "Microscopic Examination",
        "parameter": "WBC",
        "normal_range": "0-5 per hpf"
    },
    {
        "category": "Urinalysis",
        "test_name": "Microscopic Examination",
        "parameter": "Epithelial Cells",
        "normal_range": "Few (0-5 per hpf)"
    },
    {
        "category": "Urinalysis",
        "test_name": "Microscopic Examination",
        "parameter": "Bacteria",
        "normal_range": "None to few"
    },
    {
        "category": "Urinalysis",
        "test_name": "Microscopic Examination",
        "parameter": "Yeast",
        "normal_range": "None"
    },
    {
        "category": "Urinalysis",
        "test_name": "Microscopic Examination",
        "parameter": "Crystals",
        "normal_range": "None to few"
    },
    {
        "category": "Urinalysis",
        "test_name": "Microscopic Examination",
        "parameter": "Casts",
        "normal_range": "0-2 hyaline casts per lpf"
    },
    {
        "category": "Urinalysis",
        "test_name": "Microscopic Examination",
        "parameter": "Mucus",
        "normal_range": "None to few"
    },
    
    # Additional Parameters
    {
        "category": "Urinalysis",
        "test_name": "Additional Tests",
        "parameter": "Albumin",
        "normal_range": "<20 mg/L"
    },
    {
        "category": "Urinalysis",
        "test_name": "Additional Tests",
        "parameter": "Creatinine",
        "normal_range": "30-300 mg/dL"
    },
    {
        "category": "Urinalysis",
        "test_name": "Additional Tests",
        "parameter": "Microalbumin",
        "normal_range": "<30 mg/g creatinine"
    },
    {
        "category": "Urinalysis",
        "test_name": "Additional Tests",
        "parameter": "Protein/Creatinine Ratio",
        "normal_range": "<0.2 mg/mg"
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

def insert_urinalysis_data():
    """Main function to insert all urinalysis data."""
    db = SessionLocal()
    
    try:
        print("Starting urinalysis data insertion...")
        print("-" * 50)
        
        # Get or create the category
        category = get_or_create_category(db, "Urinalysis")
        
        # Insert each test
        inserted_count = 0
        skipped_count = 0
        
        for data in URINALYSIS_DATA:
            test = create_test(
                db=db,
                category_id=category.id,
                test_name=data["test_name"],
                parameter=data["parameter"],
                normal_range=data["normal_range"],
                price=0.0  # You can modify this default price
            )
            if test:
                # Check if this was a new insertion or existing test
                if "Created new test:" in str(test):
                    inserted_count += 1
                else:
                    skipped_count += 1
        
        print("-" * 50)
        print(f"Data insertion completed!")
        print(f"Category: {category.name} (ID: {category.id})")
        print(f"Tests processed: {len(URINALYSIS_DATA)}")
        print(f"New tests created: {inserted_count}")
        if skipped_count > 0:
            print(f"Existing tests skipped: {skipped_count}")
        
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
        print("\nVerifying inserted urinalysis data:")
        print("=" * 70)
        
        category = db.query(TestCategory).filter(
            TestCategory.name == "Urinalysis"
        ).first()
        
        if category:
            tests = db.query(Test).filter(Test.category_id == category.id).all()
            
            print(f"Category: {category.name}")
            print(f"Total tests in category: {len(tests)}")
            print("-" * 70)
            
            # Group tests by test type for better display
            test_groups = {}
            for test in tests:
                test_type = test.name.split(" - ")[0]
                if test_type not in test_groups:
                    test_groups[test_type] = []
                test_groups[test_type].append(test)
            
            for group_name, group_tests in test_groups.items():
                print(f"\n📋 {group_name}:")
                print("─" * 50)
                for test in group_tests:
                    parameter = test.name.split(" - ", 1)[1]
                    print(f"  • {parameter}: {test.reference_range}")
                
        else:
            print("Category 'Urinalysis' not found!")
    
    except Exception as e:
        print(f"Error occurred while verifying data: {str(e)}")
    
    finally:
        db.close()

def show_summary():
    """Show a summary of what will be inserted."""
    print("\n📊 URINALYSIS DATA SUMMARY")
    print("=" * 50)
    
    # Count tests by type
    test_types = {}
    for data in URINALYSIS_DATA:
        test_type = data["test_name"]
        if test_type not in test_types:
            test_types[test_type] = 0
        test_types[test_type] += 1
    
    print(f"Total parameters to insert: {len(URINALYSIS_DATA)}")
    print("\nBreakdown by test type:")
    for test_type, count in test_types.items():
        print(f"  • {test_type}: {count} parameters")
    print()

if __name__ == "__main__":
    print("🧪 URINALYSIS DATA INSERTION SCRIPT")
    print("="*60)
    
    # Show what will be inserted
    show_summary()
    
    # Check if tables exist, if not create them
    try:
        from database import create_tables
        create_tables()
        print("Database tables ready.")
    except Exception as e:
        print(f"Error setting up database: {str(e)}")
        sys.exit(1)
    
    # Insert the data
    insert_urinalysis_data()
    
    # Verify the inserted data
    list_inserted_data()
    
    print("\n✅ Script completed successfully!")