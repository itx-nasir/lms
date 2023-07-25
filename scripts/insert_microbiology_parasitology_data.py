#!/usr/bin/env python3
"""
Script to insert Microbiology/Parasitology test data into the LMS database.
This script will insert comprehensive microbiology and parasitology test parameters with their normal ranges.
"""

import sys
import os
# Add parent directory to path to import from database and models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import sessionmaker
from database import engine, SessionLocal
from models import TestCategory, Test

# Microbiology/Parasitology test data - typical clinical laboratory parameters
MICROBIOLOGY_PARASITOLOGY_DATA = [
    # Blood Culture
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Blood Culture",
        "parameter": "Aerobic Culture",
        "normal_range": "No growth after 5 days"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Blood Culture",
        "parameter": "Anaerobic Culture",
        "normal_range": "No growth after 5 days"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Blood Culture",
        "parameter": "Organism Identification",
        "normal_range": "No organisms isolated"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Blood Culture",
        "parameter": "Antibiotic Sensitivity",
        "normal_range": "N/A (no growth)"
    },
    
    # Urine Culture
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Urine Culture",
        "parameter": "Colony Count",
        "normal_range": "<10,000 CFU/mL"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Urine Culture",
        "parameter": "Organism Identification",
        "normal_range": "Normal flora or no significant growth"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Urine Culture",
        "parameter": "Antibiotic Sensitivity",
        "normal_range": "N/A (no significant growth)"
    },
    
    # Sputum Culture
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Sputum Culture",
        "parameter": "General Bacteria",
        "normal_range": "Normal respiratory flora"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Sputum Culture",
        "parameter": "AFB (Acid Fast Bacilli)",
        "normal_range": "No AFB seen"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Sputum Culture",
        "parameter": "TB Culture",
        "normal_range": "No growth of Mycobacterium"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Sputum Culture",
        "parameter": "Fungal Culture",
        "normal_range": "No pathogenic fungi isolated"
    },
    
    # Stool Culture
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Stool Culture",
        "parameter": "Salmonella",
        "normal_range": "Not isolated"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Stool Culture",
        "parameter": "Shigella",
        "normal_range": "Not isolated"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Stool Culture",
        "parameter": "Campylobacter",
        "normal_range": "Not isolated"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Stool Culture",
        "parameter": "E. coli O157:H7",
        "normal_range": "Not isolated"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Stool Culture",
        "parameter": "Vibrio cholerae",
        "normal_range": "Not isolated"
    },
    
    # Wound/Pus Culture
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Wound/Pus Culture",
        "parameter": "Aerobic Culture",
        "normal_range": "No growth or normal skin flora"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Wound/Pus Culture",
        "parameter": "Anaerobic Culture",
        "normal_range": "No growth"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Wound/Pus Culture",
        "parameter": "MRSA Screening",
        "normal_range": "Not detected"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Wound/Pus Culture",
        "parameter": "Antibiotic Sensitivity",
        "normal_range": "N/A (no significant growth)"
    },
    
    # Throat Culture
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Throat Culture",
        "parameter": "Group A Streptococcus",
        "normal_range": "Not isolated"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Throat Culture",
        "parameter": "Group B Streptococcus",
        "normal_range": "Not isolated"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Throat Culture",
        "parameter": "General Bacteria",
        "normal_range": "Normal throat flora"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Throat Culture",
        "parameter": "Candida Species",
        "normal_range": "Not isolated or minimal growth"
    },
    
    # Genital/Vaginal Culture
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Genital/Vaginal Culture",
        "parameter": "Neisseria gonorrhoeae",
        "normal_range": "Not isolated"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Genital/Vaginal Culture",
        "parameter": "Group B Streptococcus",
        "normal_range": "Not isolated"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Genital/Vaginal Culture",
        "parameter": "Candida Species",
        "normal_range": "Not isolated or minimal growth"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Genital/Vaginal Culture",
        "parameter": "Trichomonas vaginalis",
        "normal_range": "Not seen"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Genital/Vaginal Culture",
        "parameter": "Bacterial Vaginosis",
        "normal_range": "Negative"
    },
    
    # CSF Analysis
    {
        "category": "Microbiology / Parasitology",
        "test_name": "CSF Analysis",
        "parameter": "Bacterial Culture",
        "normal_range": "No growth"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "CSF Analysis",
        "parameter": "Fungal Culture",
        "normal_range": "No growth"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "CSF Analysis",
        "parameter": "AFB Culture",
        "normal_range": "No growth"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "CSF Analysis",
        "parameter": "Gram Stain",
        "normal_range": "No organisms seen"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "CSF Analysis",
        "parameter": "India Ink Preparation",
        "normal_range": "No Cryptococcus seen"
    },
    
    # Parasitology - Stool
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Parasitology - Stool",
        "parameter": "Ova and Parasites",
        "normal_range": "No ova or parasites seen"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Parasitology - Stool",
        "parameter": "Giardia lamblia",
        "normal_range": "Not detected"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Parasitology - Stool",
        "parameter": "Entamoeba histolytica",
        "normal_range": "Not detected"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Parasitology - Stool",
        "parameter": "Cryptosporidium",
        "normal_range": "Not detected"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Parasitology - Stool",
        "parameter": "Cyclospora",
        "normal_range": "Not detected"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Parasitology - Stool",
        "parameter": "Ascaris lumbricoides",
        "normal_range": "Not detected"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Parasitology - Stool",
        "parameter": "Hookworm",
        "normal_range": "Not detected"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Parasitology - Stool",
        "parameter": "Trichuris trichiura",
        "normal_range": "Not detected"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Parasitology - Stool",
        "parameter": "Strongyloides",
        "normal_range": "Not detected"
    },
    
    # Parasitology - Blood
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Parasitology - Blood",
        "parameter": "Malaria Parasite (Thick Film)",
        "normal_range": "No malaria parasites seen"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Parasitology - Blood",
        "parameter": "Malaria Parasite (Thin Film)",
        "normal_range": "No malaria parasites seen"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Parasitology - Blood",
        "parameter": "P. falciparum Antigen",
        "normal_range": "Negative"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Parasitology - Blood",
        "parameter": "P. vivax Antigen",
        "normal_range": "Negative"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Parasitology - Blood",
        "parameter": "Microfilaria",
        "normal_range": "Not seen"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Parasitology - Blood",
        "parameter": "Trypanosoma",
        "normal_range": "Not seen"
    },
    
    # Mycology (Fungal)
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Mycology",
        "parameter": "KOH Preparation",
        "normal_range": "No fungal elements seen"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Mycology",
        "parameter": "Fungal Culture (Skin/Hair/Nail)",
        "normal_range": "No pathogenic fungi isolated"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Mycology",
        "parameter": "Candida Culture",
        "normal_range": "Not isolated or minimal growth"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Mycology",
        "parameter": "Aspergillus Culture",
        "normal_range": "Not isolated"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Mycology",
        "parameter": "Cryptococcus Antigen",
        "normal_range": "Negative"
    },
    
    # TB/AFB Testing
    {
        "category": "Microbiology / Parasitology",
        "test_name": "TB/AFB Testing",
        "parameter": "AFB Smear (Sputum)",
        "normal_range": "No AFB seen"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "TB/AFB Testing",
        "parameter": "TB Culture",
        "normal_range": "No growth of Mycobacterium"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "TB/AFB Testing",
        "parameter": "TB PCR/GeneXpert",
        "normal_range": "MTB not detected"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "TB/AFB Testing",
        "parameter": "Drug Susceptibility",
        "normal_range": "N/A (no TB growth)"
    },
    
    # Antigen Detection
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Antigen Detection",
        "parameter": "Strep A Rapid Test",
        "normal_range": "Negative"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Antigen Detection",
        "parameter": "Legionella Antigen (Urine)",
        "normal_range": "Negative"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Antigen Detection",
        "parameter": "Pneumococcal Antigen (Urine)",
        "normal_range": "Negative"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Antigen Detection",
        "parameter": "Rotavirus Antigen",
        "normal_range": "Negative"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Antigen Detection",
        "parameter": "Adenovirus Antigen",
        "normal_range": "Negative"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Antigen Detection",
        "parameter": "Norovirus Antigen",
        "normal_range": "Negative"
    },
    
    # PCR/Molecular Testing
    {
        "category": "Microbiology / Parasitology",
        "test_name": "PCR/Molecular Testing",
        "parameter": "Chlamydia PCR",
        "normal_range": "Not detected"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "PCR/Molecular Testing",
        "parameter": "Gonorrhea PCR",
        "normal_range": "Not detected"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "PCR/Molecular Testing",
        "parameter": "HSV-1/2 PCR",
        "normal_range": "Not detected"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "PCR/Molecular Testing",
        "parameter": "CMV PCR",
        "normal_range": "Not detected"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "PCR/Molecular Testing",
        "parameter": "EBV PCR",
        "normal_range": "Not detected"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "PCR/Molecular Testing",
        "parameter": "Respiratory Panel PCR",
        "normal_range": "No pathogens detected"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "PCR/Molecular Testing",
        "parameter": "GI Panel PCR",
        "normal_range": "No pathogens detected"
    },
    
    # Special Stains
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Special Stains",
        "parameter": "Gram Stain",
        "normal_range": "No organisms seen"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Special Stains",
        "parameter": "AFB Stain",
        "normal_range": "No AFB seen"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Special Stains",
        "parameter": "PAS Stain (Fungal)",
        "normal_range": "No fungal elements seen"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Special Stains",
        "parameter": "Silver Stain",
        "normal_range": "No organisms seen"
    },
    {
        "category": "Microbiology / Parasitology",
        "test_name": "Special Stains",
        "parameter": "Calcofluor White",
        "normal_range": "No fungal elements seen"
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

def insert_microbiology_parasitology_data():
    """Main function to insert all microbiology/parasitology data."""
    db = SessionLocal()
    
    try:
        print("Starting microbiology/parasitology test data insertion...")
        print("-" * 90)
        
        # Get or create the category
        category = get_or_create_category(db, "Microbiology / Parasitology")
        
        # Insert each test
        inserted_count = 0
        
        for data in MICROBIOLOGY_PARASITOLOGY_DATA:
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
        
        print("-" * 90)
        print(f"Data insertion completed!")
        print(f"Category: {category.name} (ID: {category.id})")
        print(f"Tests processed: {len(MICROBIOLOGY_PARASITOLOGY_DATA)}")
        
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
        print("\nVerifying inserted microbiology/parasitology test data:")
        print("=" * 110)
        
        category = db.query(TestCategory).filter(
            TestCategory.name == "Microbiology / Parasitology"
        ).first()
        
        if category:
            tests = db.query(Test).filter(Test.category_id == category.id).all()
            
            print(f"Category: {category.name}")
            print(f"Total tests in category: {len(tests)}")
            print("-" * 110)
            
            # Group tests by test type for better display
            test_groups = {}
            for test in tests:
                test_type = test.name.split(" - ")[0]
                if test_type not in test_groups:
                    test_groups[test_type] = []
                test_groups[test_type].append(test)
            
            for group_name, group_tests in test_groups.items():
                print(f"\n🦠 {group_name}:")
                print("─" * 90)
                for test in group_tests:
                    parameter = test.name.split(" - ", 1)[1]
                    print(f"  • {parameter}: {test.reference_range}")
                
        else:
            print("Category 'Microbiology / Parasitology' not found!")
    
    except Exception as e:
        print(f"Error occurred while verifying data: {str(e)}")
    
    finally:
        db.close()

def show_summary():
    """Show a summary of what will be inserted."""
    print("\n🦠 MICROBIOLOGY/PARASITOLOGY TESTS DATA SUMMARY")
    print("=" * 90)
    
    # Count tests by type
    test_types = {}
    for data in MICROBIOLOGY_PARASITOLOGY_DATA:
        test_type = data["test_name"]
        if test_type not in test_types:
            test_types[test_type] = 0
        test_types[test_type] += 1
    
    print(f"Total parameters to insert: {len(MICROBIOLOGY_PARASITOLOGY_DATA)}")
    print("\nBreakdown by test type:")
    for test_type, count in test_types.items():
        print(f"  • {test_type}: {count} parameters")
    print()

if __name__ == "__main__":
    print("🦠 MICROBIOLOGY/PARASITOLOGY TESTS DATA INSERTION SCRIPT")
    print("="*100)
    
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
    insert_microbiology_parasitology_data()
    
    # Verify the inserted data
    list_inserted_data()
    
    print("\n✅ Script completed successfully!")