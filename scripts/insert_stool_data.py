#!/usr/bin/env python3
"""
Script to insert Stool/Fecal test data into the LMS database.
This script will insert comprehensive stool examination test parameters with their normal ranges.
"""

from sqlalchemy.orm import sessionmaker
from database import engine, SessionLocal
from models import TestCategory, Test
import sys

# Stool/Fecal test data - typical clinical laboratory parameters
STOOL_DATA = [
    # Physical Examination
    {
        "category": "Stool / Fecal Tests",
        "test_name": "Physical Examination",
        "parameter": "Color",
        "normal_range": "Brown"
    },
    {
        "category": "Stool / Fecal Tests",
        "test_name": "Physical Examination",
        "parameter": "Consistency",
        "normal_range": "Formed/Semi-formed"
    },
    {
        "category": "Stool / Fecal Tests",
        "test_name": "Physical Examination",
        "parameter": "Odor",
        "normal_range": "Characteristic/Not offensive"
    },
    {
        "category": "Stool / Fecal Tests",
        "test_name": "Physical Examination",
        "parameter": "Mucus",
        "normal_range": "Absent"
    },
    {
        "category": "Stool / Fecal Tests",
        "test_name": "Physical Examination",
        "parameter": "Blood",
        "normal_range": "Absent"
    },
    
    # Chemical Examination
    {
        "category": "Stool / Fecal Tests",
        "test_name": "Chemical Examination",
        "parameter": "pH",
        "normal_range": "6.0-8.0"
    },
    {
        "category": "Stool / Fecal Tests",
        "test_name": "Chemical Examination",
        "parameter": "Occult Blood",
        "normal_range": "Negative"
    },
    {
        "category": "Stool / Fecal Tests",
        "test_name": "Chemical Examination",
        "parameter": "Reducing Substances",
        "normal_range": "Negative (<0.25%)"
    },
    {
        "category": "Stool / Fecal Tests",
        "test_name": "Chemical Examination",
        "parameter": "Fat Globules",
        "normal_range": "Absent or few"
    },
    
    # Microscopic Examination
    {
        "category": "Stool / Fecal Tests",
        "test_name": "Microscopic Examination",
        "parameter": "RBC",
        "normal_range": "Absent"
    },
    {
        "category": "Stool / Fecal Tests",
        "test_name": "Microscopic Examination",
        "parameter": "WBC",
        "normal_range": "0-2 per hpf"
    },
    {
        "category": "Stool / Fecal Tests",
        "test_name": "Microscopic Examination",
        "parameter": "Epithelial Cells",
        "normal_range": "Few"
    },
    {
        "category": "Stool / Fecal Tests",
        "test_name": "Microscopic Examination",
        "parameter": "Bacteria",
        "normal_range": "Normal flora present"
    },
    {
        "category": "Stool / Fecal Tests",
        "test_name": "Microscopic Examination",
        "parameter": "Yeast",
        "normal_range": "Absent or few"
    },
    {
        "category": "Stool / Fecal Tests",
        "test_name": "Microscopic Examination",
        "parameter": "Parasites",
        "normal_range": "None seen"
    },
    {
        "category": "Stool / Fecal Tests",
        "test_name": "Microscopic Examination",
        "parameter": "Ova",
        "normal_range": "None seen"
    },
    {
        "category": "Stool / Fecal Tests",
        "test_name": "Microscopic Examination",
        "parameter": "Cysts",
        "normal_range": "None seen"
    },
    
    # Parasitology
    {
        "category": "Stool / Fecal Tests",
        "test_name": "Parasitology",
        "parameter": "Giardia Antigen",
        "normal_range": "Negative"
    },
    {
        "category": "Stool / Fecal Tests",
        "test_name": "Parasitology",
        "parameter": "Cryptosporidium Antigen",
        "normal_range": "Negative"
    },
    {
        "category": "Stool / Fecal Tests",
        "test_name": "Parasitology",
        "parameter": "E. histolytica Antigen",
        "normal_range": "Negative"
    },
    
    # Bacteriology
    {
        "category": "Stool / Fecal Tests",
        "test_name": "Bacteriology",
        "parameter": "Salmonella",
        "normal_range": "Not isolated"
    },
    {
        "category": "Stool / Fecal Tests",
        "test_name": "Bacteriology",
        "parameter": "Shigella",
        "normal_range": "Not isolated"
    },
    {
        "category": "Stool / Fecal Tests",
        "test_name": "Bacteriology",
        "parameter": "Campylobacter",
        "normal_range": "Not isolated"
    },
    {
        "category": "Stool / Fecal Tests",
        "test_name": "Bacteriology",
        "parameter": "E. coli O157:H7",
        "normal_range": "Not isolated"
    },
    {
        "category": "Stool / Fecal Tests",
        "test_name": "Bacteriology",
        "parameter": "C. difficile Toxin A/B",
        "normal_range": "Negative"
    },
    
    # Inflammatory Markers
    {
        "category": "Stool / Fecal Tests",
        "test_name": "Inflammatory Markers",
        "parameter": "Fecal Calprotectin",
        "normal_range": "<50 µg/g (adults); <150 µg/g (children)"
    },
    {
        "category": "Stool / Fecal Tests",
        "test_name": "Inflammatory Markers",
        "parameter": "Fecal Lactoferrin",
        "normal_range": "<7.25 µg/mL"
    },
    
    # Fat Analysis
    {
        "category": "Stool / Fecal Tests",
        "test_name": "Fat Analysis",
        "parameter": "Fecal Fat (Qualitative)",
        "normal_range": "Negative for excess fat"
    },
    {
        "category": "Stool / Fecal Tests",
        "test_name": "Fat Analysis",
        "parameter": "Fecal Fat (72-hour)",
        "normal_range": "<7 g/24 hours"
    },
    {
        "category": "Stool / Fecal Tests",
        "test_name": "Fat Analysis",
        "parameter": "Coefficient of Fat Absorption",
        "normal_range": ">93%"
    },
    
    # Additional Tests
    {
        "category": "Stool / Fecal Tests",
        "test_name": "Additional Tests",
        "parameter": "Alpha-1-Antitrypsin",
        "normal_range": "<27.5 mg/dL"
    },
    {
        "category": "Stool / Fecal Tests",
        "test_name": "Additional Tests",
        "parameter": "Elastase-1",
        "normal_range": ">200 µg/g"
    },
    {
        "category": "Stool / Fecal Tests",
        "test_name": "Additional Tests",
        "parameter": "Chymotrypsin",
        "normal_range": ">120 U/g"
    },
    {
        "category": "Stool / Fecal Tests",
        "test_name": "Additional Tests",
        "parameter": "Trypsin",
        "normal_range": "Present (in children)"
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

def insert_stool_data():
    """Main function to insert all stool test data."""
    db = SessionLocal()
    
    try:
        print("Starting stool/fecal test data insertion...")
        print("-" * 60)
        
        # Get or create the category
        category = get_or_create_category(db, "Stool / Fecal Tests")
        
        # Insert each test
        inserted_count = 0
        skipped_count = 0
        
        for data in STOOL_DATA:
            test = create_test(
                db=db,
                category_id=category.id,
                test_name=data["test_name"],
                parameter=data["parameter"],
                normal_range=data["normal_range"],
                price=0.0  # You can modify this default price
            )
            if test:
                # Check if this was a new insertion by checking the print output
                # This is a simple way to track new vs existing
                inserted_count += 1
        
        print("-" * 60)
        print(f"Data insertion completed!")
        print(f"Category: {category.name} (ID: {category.id})")
        print(f"Tests processed: {len(STOOL_DATA)}")
        
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
        print("\nVerifying inserted stool/fecal test data:")
        print("=" * 80)
        
        category = db.query(TestCategory).filter(
            TestCategory.name == "Stool / Fecal Tests"
        ).first()
        
        if category:
            tests = db.query(Test).filter(Test.category_id == category.id).all()
            
            print(f"Category: {category.name}")
            print(f"Total tests in category: {len(tests)}")
            print("-" * 80)
            
            # Group tests by test type for better display
            test_groups = {}
            for test in tests:
                test_type = test.name.split(" - ")[0]
                if test_type not in test_groups:
                    test_groups[test_type] = []
                test_groups[test_type].append(test)
            
            for group_name, group_tests in test_groups.items():
                print(f"\n💩 {group_name}:")
                print("─" * 60)
                for test in group_tests:
                    parameter = test.name.split(" - ", 1)[1]
                    print(f"  • {parameter}: {test.reference_range}")
                
        else:
            print("Category 'Stool / Fecal Tests' not found!")
    
    except Exception as e:
        print(f"Error occurred while verifying data: {str(e)}")
    
    finally:
        db.close()

def show_summary():
    """Show a summary of what will be inserted."""
    print("\n💩 STOOL/FECAL TESTS DATA SUMMARY")
    print("=" * 60)
    
    # Count tests by type
    test_types = {}
    for data in STOOL_DATA:
        test_type = data["test_name"]
        if test_type not in test_types:
            test_types[test_type] = 0
        test_types[test_type] += 1
    
    print(f"Total parameters to insert: {len(STOOL_DATA)}")
    print("\nBreakdown by test type:")
    for test_type, count in test_types.items():
        print(f"  • {test_type}: {count} parameters")
    print()

if __name__ == "__main__":
    print("💩 STOOL/FECAL TESTS DATA INSERTION SCRIPT")
    print("="*70)
    
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
    insert_stool_data()
    
    # Verify the inserted data
    list_inserted_data()
    
    print("\n✅ Script completed successfully!")