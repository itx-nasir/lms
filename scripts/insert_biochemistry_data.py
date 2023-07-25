#!/usr/bin/env python3
"""
Script to insert Biochemistry test data into the LMS database.
This script will insert comprehensive biochemistry test parameters with their normal ranges.
"""

import sys
import os
# Add parent directory to path to import from database and models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import sessionmaker
from database import engine, SessionLocal
from models import TestCategory, Test

# Biochemistry test data - typical clinical laboratory parameters
BIOCHEMISTRY_DATA = [
    # Liver Function Tests
    {
        "category": "Biochemistry",
        "test_name": "Liver Function Tests",
        "parameter": "ALT (SGPT)",
        "normal_range": "M: 7-56 U/L; F: 7-40 U/L"
    },
    {
        "category": "Biochemistry",
        "test_name": "Liver Function Tests",
        "parameter": "AST (SGOT)",
        "normal_range": "M: 10-40 U/L; F: 9-32 U/L"
    },
    {
        "category": "Biochemistry",
        "test_name": "Liver Function Tests",
        "parameter": "ALP (Alkaline Phosphatase)",
        "normal_range": "Adults: 44-147 U/L"
    },
    {
        "category": "Biochemistry",
        "test_name": "Liver Function Tests",
        "parameter": "GGT (Gamma GT)",
        "normal_range": "M: 11-50 U/L; F: 7-32 U/L"
    },
    {
        "category": "Biochemistry",
        "test_name": "Liver Function Tests",
        "parameter": "Total Bilirubin",
        "normal_range": "0.2-1.2 mg/dL (3.4-20.5 µmol/L)"
    },
    {
        "category": "Biochemistry",
        "test_name": "Liver Function Tests",
        "parameter": "Direct Bilirubin",
        "normal_range": "0.0-0.3 mg/dL (0-5.1 µmol/L)"
    },
    {
        "category": "Biochemistry",
        "test_name": "Liver Function Tests",
        "parameter": "Indirect Bilirubin",
        "normal_range": "0.2-0.8 mg/dL (3.4-13.7 µmol/L)"
    },
    {
        "category": "Biochemistry",
        "test_name": "Liver Function Tests",
        "parameter": "Total Protein",
        "normal_range": "6.0-8.3 g/dL (60-83 g/L)"
    },
    {
        "category": "Biochemistry",
        "test_name": "Liver Function Tests",
        "parameter": "Albumin",
        "normal_range": "3.5-5.0 g/dL (35-50 g/L)"
    },
    {
        "category": "Biochemistry",
        "test_name": "Liver Function Tests",
        "parameter": "Globulin",
        "normal_range": "2.3-3.5 g/dL (23-35 g/L)"
    },
    {
        "category": "Biochemistry",
        "test_name": "Liver Function Tests",
        "parameter": "A/G Ratio",
        "normal_range": "1.1-2.5"
    },
    
    # Kidney Function Tests
    {
        "category": "Biochemistry",
        "test_name": "Kidney Function Tests",
        "parameter": "Urea",
        "normal_range": "15-45 mg/dL (2.5-7.5 mmol/L)"
    },
    {
        "category": "Biochemistry",
        "test_name": "Kidney Function Tests",
        "parameter": "Creatinine",
        "normal_range": "M: 0.7-1.3 mg/dL; F: 0.6-1.1 mg/dL"
    },
    {
        "category": "Biochemistry",
        "test_name": "Kidney Function Tests",
        "parameter": "BUN",
        "normal_range": "7-20 mg/dL (2.5-7.1 mmol/L)"
    },
    {
        "category": "Biochemistry",
        "test_name": "Kidney Function Tests",
        "parameter": "eGFR",
        "normal_range": ">90 mL/min/1.73m²"
    },
    {
        "category": "Biochemistry",
        "test_name": "Kidney Function Tests",
        "parameter": "Uric Acid",
        "normal_range": "M: 3.4-7.0 mg/dL; F: 2.4-6.0 mg/dL"
    },
    
    # Lipid Profile
    {
        "category": "Biochemistry",
        "test_name": "Lipid Profile",
        "parameter": "Total Cholesterol",
        "normal_range": "<200 mg/dL (<5.2 mmol/L)"
    },
    {
        "category": "Biochemistry",
        "test_name": "Lipid Profile",
        "parameter": "HDL Cholesterol",
        "normal_range": "M: >40 mg/dL; F: >50 mg/dL"
    },
    {
        "category": "Biochemistry",
        "test_name": "Lipid Profile",
        "parameter": "LDL Cholesterol",
        "normal_range": "<100 mg/dL (<2.6 mmol/L)"
    },
    {
        "category": "Biochemistry",
        "test_name": "Lipid Profile",
        "parameter": "VLDL Cholesterol",
        "normal_range": "5-40 mg/dL (0.1-1.0 mmol/L)"
    },
    {
        "category": "Biochemistry",
        "test_name": "Lipid Profile",
        "parameter": "Triglycerides",
        "normal_range": "<150 mg/dL (<1.7 mmol/L)"
    },
    {
        "category": "Biochemistry",
        "test_name": "Lipid Profile",
        "parameter": "Non-HDL Cholesterol",
        "normal_range": "<130 mg/dL (<3.4 mmol/L)"
    },
    {
        "category": "Biochemistry",
        "test_name": "Lipid Profile",
        "parameter": "TC/HDL Ratio",
        "normal_range": "<5.0"
    },
    
    # Diabetes Panel
    {
        "category": "Biochemistry",
        "test_name": "Diabetes Panel",
        "parameter": "Glucose (Fasting)",
        "normal_range": "70-100 mg/dL (3.9-5.6 mmol/L)"
    },
    {
        "category": "Biochemistry",
        "test_name": "Diabetes Panel",
        "parameter": "Glucose (Random)",
        "normal_range": "70-140 mg/dL (3.9-7.8 mmol/L)"
    },
    {
        "category": "Biochemistry",
        "test_name": "Diabetes Panel",
        "parameter": "HbA1c",
        "normal_range": "<5.7% (<39 mmol/mol)"
    },
    {
        "category": "Biochemistry",
        "test_name": "Diabetes Panel",
        "parameter": "Fructosamine",
        "normal_range": "205-285 µmol/L"
    },
    
    # Electrolytes
    {
        "category": "Biochemistry",
        "test_name": "Electrolytes",
        "parameter": "Sodium",
        "normal_range": "136-145 mmol/L"
    },
    {
        "category": "Biochemistry",
        "test_name": "Electrolytes",
        "parameter": "Potassium",
        "normal_range": "3.5-5.1 mmol/L"
    },
    {
        "category": "Biochemistry",
        "test_name": "Electrolytes",
        "parameter": "Chloride",
        "normal_range": "98-107 mmol/L"
    },
    {
        "category": "Biochemistry",
        "test_name": "Electrolytes",
        "parameter": "CO2 (Bicarbonate)",
        "normal_range": "22-29 mmol/L"
    },
    {
        "category": "Biochemistry",
        "test_name": "Electrolytes",
        "parameter": "Anion Gap",
        "normal_range": "8-16 mmol/L"
    },
    
    # Cardiac Markers
    {
        "category": "Biochemistry",
        "test_name": "Cardiac Markers",
        "parameter": "CK-Total",
        "normal_range": "M: 39-308 U/L; F: 26-192 U/L"
    },
    {
        "category": "Biochemistry",
        "test_name": "Cardiac Markers",
        "parameter": "CK-MB",
        "normal_range": "0-6.3 ng/mL"
    },
    {
        "category": "Biochemistry",
        "test_name": "Cardiac Markers",
        "parameter": "Troponin I",
        "normal_range": "<0.04 ng/mL"
    },
    {
        "category": "Biochemistry",
        "test_name": "Cardiac Markers",
        "parameter": "Troponin T",
        "normal_range": "<0.01 ng/mL"
    },
    {
        "category": "Biochemistry",
        "test_name": "Cardiac Markers",
        "parameter": "LDH",
        "normal_range": "140-280 U/L"
    },
    
    # Bone Markers
    {
        "category": "Biochemistry",
        "test_name": "Bone Markers",
        "parameter": "Calcium (Total)",
        "normal_range": "8.5-10.5 mg/dL (2.1-2.6 mmol/L)"
    },
    {
        "category": "Biochemistry",
        "test_name": "Bone Markers",
        "parameter": "Calcium (Ionized)",
        "normal_range": "4.65-5.25 mg/dL (1.16-1.31 mmol/L)"
    },
    {
        "category": "Biochemistry",
        "test_name": "Bone Markers",
        "parameter": "Phosphorus",
        "normal_range": "2.5-4.5 mg/dL (0.8-1.5 mmol/L)"
    },
    {
        "category": "Biochemistry",
        "test_name": "Bone Markers",
        "parameter": "Magnesium",
        "normal_range": "1.7-2.2 mg/dL (0.7-0.9 mmol/L)"
    },
    
    # Iron Studies
    {
        "category": "Biochemistry",
        "test_name": "Iron Studies",
        "parameter": "Iron",
        "normal_range": "M: 65-175 µg/dL; F: 50-170 µg/dL"
    },
    {
        "category": "Biochemistry",
        "test_name": "Iron Studies",
        "parameter": "TIBC",
        "normal_range": "250-450 µg/dL"
    },
    {
        "category": "Biochemistry",
        "test_name": "Iron Studies",
        "parameter": "Transferrin Saturation",
        "normal_range": "20-50%"
    },
    {
        "category": "Biochemistry",
        "test_name": "Iron Studies",
        "parameter": "Ferritin",
        "normal_range": "M: 12-300 ng/mL; F: 12-150 ng/mL"
    },
    
    # Pancreatic Enzymes
    {
        "category": "Biochemistry",
        "test_name": "Pancreatic Enzymes",
        "parameter": "Amylase",
        "normal_range": "28-100 U/L"
    },
    {
        "category": "Biochemistry",
        "test_name": "Pancreatic Enzymes",
        "parameter": "Lipase",
        "normal_range": "10-140 U/L"
    },
    
    # Inflammatory Markers
    {
        "category": "Biochemistry",
        "test_name": "Inflammatory Markers",
        "parameter": "CRP",
        "normal_range": "<3.0 mg/L"
    },
    {
        "category": "Biochemistry",
        "test_name": "Inflammatory Markers",
        "parameter": "ESR",
        "normal_range": "M: <15 mm/hr; F: <20 mm/hr"
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

def insert_biochemistry_data():
    """Main function to insert all biochemistry data."""
    db = SessionLocal()
    
    try:
        print("Starting biochemistry test data insertion...")
        print("-" * 70)
        
        # Get or create the category
        category = get_or_create_category(db, "Biochemistry")
        
        # Insert each test
        inserted_count = 0
        
        for data in BIOCHEMISTRY_DATA:
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
        
        print("-" * 70)
        print(f"Data insertion completed!")
        print(f"Category: {category.name} (ID: {category.id})")
        print(f"Tests processed: {len(BIOCHEMISTRY_DATA)}")
        
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
        print("\nVerifying inserted biochemistry test data:")
        print("=" * 90)
        
        category = db.query(TestCategory).filter(
            TestCategory.name == "Biochemistry"
        ).first()
        
        if category:
            tests = db.query(Test).filter(Test.category_id == category.id).all()
            
            print(f"Category: {category.name}")
            print(f"Total tests in category: {len(tests)}")
            print("-" * 90)
            
            # Group tests by test type for better display
            test_groups = {}
            for test in tests:
                test_type = test.name.split(" - ")[0]
                if test_type not in test_groups:
                    test_groups[test_type] = []
                test_groups[test_type].append(test)
            
            for group_name, group_tests in test_groups.items():
                print(f"\n🧪 {group_name}:")
                print("─" * 70)
                for test in group_tests:
                    parameter = test.name.split(" - ", 1)[1]
                    print(f"  • {parameter}: {test.reference_range}")
                
        else:
            print("Category 'Biochemistry' not found!")
    
    except Exception as e:
        print(f"Error occurred while verifying data: {str(e)}")
    
    finally:
        db.close()

def show_summary():
    """Show a summary of what will be inserted."""
    print("\n🧪 BIOCHEMISTRY TESTS DATA SUMMARY")
    print("=" * 70)
    
    # Count tests by type
    test_types = {}
    for data in BIOCHEMISTRY_DATA:
        test_type = data["test_name"]
        if test_type not in test_types:
            test_types[test_type] = 0
        test_types[test_type] += 1
    
    print(f"Total parameters to insert: {len(BIOCHEMISTRY_DATA)}")
    print("\nBreakdown by test type:")
    for test_type, count in test_types.items():
        print(f"  • {test_type}: {count} parameters")
    print()

if __name__ == "__main__":
    print("🧪 BIOCHEMISTRY TESTS DATA INSERTION SCRIPT")
    print("="*80)
    
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
    insert_biochemistry_data()
    
    # Verify the inserted data
    list_inserted_data()
    
    print("\n✅ Script completed successfully!")