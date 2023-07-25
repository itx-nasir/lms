#!/usr/bin/env python3
"""
Script to insert Immunology/Serology test data into the LMS database.
This script will insert comprehensive immunology and serology test parameters with their normal ranges.
"""

import sys
import os
# Add parent directory to path to import from database and models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import sessionmaker
from database import engine, SessionLocal
from models import TestCategory, Test

# Immunology/Serology test data - typical clinical laboratory parameters
IMMUNOLOGY_SEROLOGY_DATA = [
    # Hepatitis Panel
    {
        "category": "Immunology / Serology",
        "test_name": "Hepatitis Panel",
        "parameter": "HBsAg",
        "normal_range": "Non-reactive"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Hepatitis Panel",
        "parameter": "Anti-HBs",
        "normal_range": "Non-reactive or >10 mIU/mL (immune)"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Hepatitis Panel",
        "parameter": "Anti-HBc Total",
        "normal_range": "Non-reactive"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Hepatitis Panel",
        "parameter": "Anti-HBc IgM",
        "normal_range": "Non-reactive"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Hepatitis Panel",
        "parameter": "HBeAg",
        "normal_range": "Non-reactive"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Hepatitis Panel",
        "parameter": "Anti-HBe",
        "normal_range": "Non-reactive"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Hepatitis Panel",
        "parameter": "Anti-HCV",
        "normal_range": "Non-reactive"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Hepatitis Panel",
        "parameter": "Anti-HAV IgM",
        "normal_range": "Non-reactive"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Hepatitis Panel",
        "parameter": "Anti-HAV IgG",
        "normal_range": "Non-reactive"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Hepatitis Panel",
        "parameter": "Anti-HEV IgM",
        "normal_range": "Non-reactive"
    },
    
    # HIV Testing
    {
        "category": "Immunology / Serology",
        "test_name": "HIV Testing",
        "parameter": "HIV 1 & 2 Ab",
        "normal_range": "Non-reactive"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "HIV Testing",
        "parameter": "HIV Ag/Ab Combo",
        "normal_range": "Non-reactive"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "HIV Testing",
        "parameter": "HIV-1 RNA (Viral Load)",
        "normal_range": "Not detected"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "HIV Testing",
        "parameter": "CD4+ Count",
        "normal_range": "500-1600 cells/µL"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "HIV Testing",
        "parameter": "CD4/CD8 Ratio",
        "normal_range": "1.0-4.0"
    },
    
    # TORCH Panel
    {
        "category": "Immunology / Serology",
        "test_name": "TORCH Panel",
        "parameter": "Toxoplasma IgG",
        "normal_range": "<1.6 IU/mL (negative)"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "TORCH Panel",
        "parameter": "Toxoplasma IgM",
        "normal_range": "<0.55 (negative)"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "TORCH Panel",
        "parameter": "Rubella IgG",
        "normal_range": "<10 IU/mL (non-immune); >15 IU/mL (immune)"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "TORCH Panel",
        "parameter": "Rubella IgM",
        "normal_range": "<0.9 (negative)"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "TORCH Panel",
        "parameter": "CMV IgG",
        "normal_range": "<6.0 AU/mL (negative)"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "TORCH Panel",
        "parameter": "CMV IgM",
        "normal_range": "<0.85 (negative)"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "TORCH Panel",
        "parameter": "HSV-1 IgG",
        "normal_range": "<0.9 (negative); >1.1 (positive)"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "TORCH Panel",
        "parameter": "HSV-2 IgG",
        "normal_range": "<0.9 (negative); >1.1 (positive)"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "TORCH Panel",
        "parameter": "HSV-1/2 IgM",
        "normal_range": "<0.9 (negative)"
    },
    
    # Autoimmune Markers
    {
        "category": "Immunology / Serology",
        "test_name": "Autoimmune Markers",
        "parameter": "ANA (Antinuclear Antibody)",
        "normal_range": "Negative (<1:80)"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Autoimmune Markers",
        "parameter": "Anti-dsDNA",
        "normal_range": "<25 IU/mL"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Autoimmune Markers",
        "parameter": "Anti-Sm",
        "normal_range": "<20 U/mL"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Autoimmune Markers",
        "parameter": "Anti-SSA/Ro52",
        "normal_range": "<20 U/mL"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Autoimmune Markers",
        "parameter": "Anti-SSB/La",
        "normal_range": "<20 U/mL"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Autoimmune Markers",
        "parameter": "Anti-Scl-70",
        "normal_range": "<20 U/mL"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Autoimmune Markers",
        "parameter": "Anti-Jo-1",
        "normal_range": "<20 U/mL"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Autoimmune Markers",
        "parameter": "Anti-Centromere",
        "normal_range": "<20 U/mL"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Autoimmune Markers",
        "parameter": "Anti-CCP",
        "normal_range": "<20 U/mL"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Autoimmune Markers",
        "parameter": "Rheumatoid Factor (RF)",
        "normal_range": "<15 IU/mL"
    },
    
    # Thyroid Antibodies
    {
        "category": "Immunology / Serology",
        "test_name": "Thyroid Antibodies",
        "parameter": "Anti-TPO",
        "normal_range": "<35 IU/mL"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Thyroid Antibodies",
        "parameter": "Anti-Thyroglobulin",
        "normal_range": "<40 IU/mL"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Thyroid Antibodies",
        "parameter": "TSI (TSH Receptor Ab)",
        "normal_range": "<1.75 IU/L"
    },
    
    # Celiac Disease
    {
        "category": "Immunology / Serology",
        "test_name": "Celiac Disease",
        "parameter": "Anti-tTG IgA",
        "normal_range": "<10 U/mL"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Celiac Disease",
        "parameter": "Anti-tTG IgG",
        "normal_range": "<10 U/mL"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Celiac Disease",
        "parameter": "Anti-Endomysial IgA",
        "normal_range": "Negative"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Celiac Disease",
        "parameter": "Anti-Gliadin IgG",
        "normal_range": "<25 U/mL"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Celiac Disease",
        "parameter": "Total IgA",
        "normal_range": "70-400 mg/dL"
    },
    
    # Immunoglobulins
    {
        "category": "Immunology / Serology",
        "test_name": "Immunoglobulins",
        "parameter": "IgG",
        "normal_range": "700-1600 mg/dL"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Immunoglobulins",
        "parameter": "IgA",
        "normal_range": "70-400 mg/dL"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Immunoglobulins",
        "parameter": "IgM",
        "normal_range": "40-230 mg/dL"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Immunoglobulins",
        "parameter": "IgE Total",
        "normal_range": "<100 IU/mL (adults)"
    },
    
    # Complement System
    {
        "category": "Immunology / Serology",
        "test_name": "Complement System",
        "parameter": "C3",
        "normal_range": "90-180 mg/dL"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Complement System",
        "parameter": "C4",
        "normal_range": "10-40 mg/dL"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Complement System",
        "parameter": "CH50",
        "normal_range": "60-144 CAE units"
    },
    
    # Bacterial Serology
    {
        "category": "Immunology / Serology",
        "test_name": "Bacterial Serology",
        "parameter": "ASO (Anti-Streptolysin O)",
        "normal_range": "<200 IU/mL"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Bacterial Serology",
        "parameter": "H. pylori IgG",
        "normal_range": "<0.75 (negative)"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Bacterial Serology",
        "parameter": "Brucella Ab",
        "normal_range": "<1:80 (negative)"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Bacterial Serology",
        "parameter": "Salmonella Typhi O",
        "normal_range": "<1:80 (negative)"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Bacterial Serology",
        "parameter": "Salmonella Typhi H",
        "normal_range": "<1:80 (negative)"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Bacterial Serology",
        "parameter": "Salmonella Paratyphi A",
        "normal_range": "<1:80 (negative)"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Bacterial Serology",
        "parameter": "Salmonella Paratyphi B",
        "normal_range": "<1:80 (negative)"
    },
    
    # Syphilis Testing
    {
        "category": "Immunology / Serology",
        "test_name": "Syphilis Testing",
        "parameter": "VDRL",
        "normal_range": "Non-reactive"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Syphilis Testing",
        "parameter": "TPHA",
        "normal_range": "Non-reactive"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Syphilis Testing",
        "parameter": "FTA-ABS",
        "normal_range": "Non-reactive"
    },
    
    # Dengue Serology
    {
        "category": "Immunology / Serology",
        "test_name": "Dengue Serology",
        "parameter": "Dengue NS1 Antigen",
        "normal_range": "Negative"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Dengue Serology",
        "parameter": "Dengue IgM",
        "normal_range": "Negative"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Dengue Serology",
        "parameter": "Dengue IgG",
        "normal_range": "Negative"
    },
    
    # Other Viral Serology
    {
        "category": "Immunology / Serology",
        "test_name": "Other Viral Serology",
        "parameter": "EBV VCA IgM",
        "normal_range": "<0.8 (negative)"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Other Viral Serology",
        "parameter": "EBV VCA IgG",
        "normal_range": "<0.8 (negative)"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Other Viral Serology",
        "parameter": "EBV EBNA IgG",
        "normal_range": "<0.8 (negative)"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Other Viral Serology",
        "parameter": "Varicella Zoster IgG",
        "normal_range": "<0.9 (negative); >1.1 (immune)"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "Other Viral Serology",
        "parameter": "Varicella Zoster IgM",
        "normal_range": "<0.9 (negative)"
    },
    
    # COVID-19 Serology
    {
        "category": "Immunology / Serology",
        "test_name": "COVID-19 Serology",
        "parameter": "SARS-CoV-2 IgM",
        "normal_range": "Negative"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "COVID-19 Serology",
        "parameter": "SARS-CoV-2 IgG",
        "normal_range": "Negative"
    },
    {
        "category": "Immunology / Serology",
        "test_name": "COVID-19 Serology",
        "parameter": "SARS-CoV-2 Total Ab",
        "normal_range": "Negative"
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

def insert_immunology_serology_data():
    """Main function to insert all immunology/serology data."""
    db = SessionLocal()
    
    try:
        print("Starting immunology/serology test data insertion...")
        print("-" * 80)
        
        # Get or create the category
        category = get_or_create_category(db, "Immunology / Serology")
        
        # Insert each test
        inserted_count = 0
        
        for data in IMMUNOLOGY_SEROLOGY_DATA:
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
        
        print("-" * 80)
        print(f"Data insertion completed!")
        print(f"Category: {category.name} (ID: {category.id})")
        print(f"Tests processed: {len(IMMUNOLOGY_SEROLOGY_DATA)}")
        
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
        print("\nVerifying inserted immunology/serology test data:")
        print("=" * 100)
        
        category = db.query(TestCategory).filter(
            TestCategory.name == "Immunology / Serology"
        ).first()
        
        if category:
            tests = db.query(Test).filter(Test.category_id == category.id).all()
            
            print(f"Category: {category.name}")
            print(f"Total tests in category: {len(tests)}")
            print("-" * 100)
            
            # Group tests by test type for better display
            test_groups = {}
            for test in tests:
                test_type = test.name.split(" - ")[0]
                if test_type not in test_groups:
                    test_groups[test_type] = []
                test_groups[test_type].append(test)
            
            for group_name, group_tests in test_groups.items():
                print(f"\n🧬 {group_name}:")
                print("─" * 80)
                for test in group_tests:
                    parameter = test.name.split(" - ", 1)[1]
                    print(f"  • {parameter}: {test.reference_range}")
                
        else:
            print("Category 'Immunology / Serology' not found!")
    
    except Exception as e:
        print(f"Error occurred while verifying data: {str(e)}")
    
    finally:
        db.close()

def show_summary():
    """Show a summary of what will be inserted."""
    print("\n🧬 IMMUNOLOGY/SEROLOGY TESTS DATA SUMMARY")
    print("=" * 80)
    
    # Count tests by type
    test_types = {}
    for data in IMMUNOLOGY_SEROLOGY_DATA:
        test_type = data["test_name"]
        if test_type not in test_types:
            test_types[test_type] = 0
        test_types[test_type] += 1
    
    print(f"Total parameters to insert: {len(IMMUNOLOGY_SEROLOGY_DATA)}")
    print("\nBreakdown by test type:")
    for test_type, count in test_types.items():
        print(f"  • {test_type}: {count} parameters")
    print()

if __name__ == "__main__":
    print("🧬 IMMUNOLOGY/SEROLOGY TESTS DATA INSERTION SCRIPT")
    print("="*90)
    
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
    insert_immunology_serology_data()
    
    # Verify the inserted data
    list_inserted_data()
    
    print("\n✅ Script completed successfully!")