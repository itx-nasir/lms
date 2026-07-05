#!/usr/bin/env python3
"""
Unified data seeding script for LMS.
Creates admin user and inserts all test data (idempotent).
Run: python seed_data.py
"""

import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import create_tables, SessionLocal
import crud
from models import TestCategory, Test, Panel, PanelTest

load_dotenv()

# ============================================================
# 1. ADMIN SEEDING
# ============================================================
def seed_admin():
    """Create or update admin user from environment variables."""
    db = SessionLocal()
    try:
        admin_username = os.getenv('ADMIN_USERNAME', 'admin')
        admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')

        existing = crud.get_admin_user(db, admin_username)
        if existing:
            print(f"Admin user '{admin_username}' already exists (id={existing.id}).")
        else:
            crud.create_admin_user(db, admin_username, admin_password)
            print(f"Created admin user: {admin_username}")
    finally:
        db.close()

# ============================================================
# 2. TEST DATA DEFINITION
# ============================================================
ALL_TEST_DATA = [
    # ---------- Biochemistry ----------
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
    },

    # ---------- Haematology & Coagulation ----------
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
    },

    # ---------- Immunology / Serology ----------
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
    },

    # ---------- Microbiology / Parasitology ----------
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
    },

    # ---------- Stool / Fecal Tests ----------
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
    },

    # ---------- Urinalysis ----------
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
    },
]

# ============================================================
# 3. HELPER FUNCTIONS (shared)
# ============================================================
def get_or_create_category(db, category_name):
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

def get_or_create_panel(db, panel_name):
    panel = db.query(Panel).filter(Panel.name == panel_name).first()
    if not panel:
        panel = Panel(name=panel_name, price=0.0)
        db.add(panel)
        db.commit()
        db.refresh(panel)
        print(f"Created new panel: {panel_name}")
    return panel

def create_test_in_panel(db, category_id, panel_id, parameter, normal_range, price=0.0):
    """Create the parameter as a Test and link it to its Panel, unless it
    already exists (idempotent so the script can be re-run safely)."""
    existing = (
        db.query(Test)
        .join(PanelTest, PanelTest.test_id == Test.id)
        .filter(PanelTest.panel_id == panel_id, Test.name == parameter)
        .first()
    )
    if existing:
        print(f"Test already exists: {parameter} (panel #{panel_id})")
        return existing

    new_test = Test(
        name=parameter,
        price=price,
        reference_range=normal_range,
        category_id=category_id
    )
    db.add(new_test)
    db.commit()
    db.refresh(new_test)

    sequence = db.query(PanelTest).filter(PanelTest.panel_id == panel_id).count()
    db.add(PanelTest(panel_id=panel_id, test_id=new_test.id, sequence=sequence))
    db.commit()

    print(f"Created new test: {parameter} (panel #{panel_id})")
    return new_test

# ============================================================
# 4. MAIN INSERTION LOGIC
# ============================================================
def seed_tests():
    db = SessionLocal()
    try:
        print("\n" + "=" * 80)
        print("SEEDING TEST DATA")
        print("=" * 80)

        # Create categories first
        categories = set(item["category"] for item in ALL_TEST_DATA)
        category_map = {}
        for cat_name in categories:
            cat = get_or_create_category(db, cat_name)
            category_map[cat_name] = cat.id

        # Some generic group names (e.g. "Physical Examination", "Chemical
        # Examination", "Inflammatory Markers") are reused across different
        # categories (Stool vs Urinalysis, Biochemistry vs Stool, etc). Each
        # occurrence must become its OWN panel, so disambiguate the display
        # name with the category whenever a (category, test_name) pair isn't
        # unique on its own.
        group_categories = {}
        for item in ALL_TEST_DATA:
            group_categories.setdefault(item["test_name"], set()).add(item["category"])

        # Create panels keyed by (category, test_name) so same-named groups
        # in different categories never collide.
        panel_map = {}  # (category, test_name) -> panel_id
        for item in ALL_TEST_DATA:
            key = (item["category"], item["test_name"])
            if key in panel_map:
                continue
            if len(group_categories[item["test_name"]]) > 1:
                display_name = f"{item['test_name']} ({item['category'].split('/')[0].split(' ')[0]})"
            else:
                display_name = item["test_name"]
            panel = get_or_create_panel(db, display_name)
            panel_map[key] = panel.id

        # Insert each test parameter, linked to its panel
        for idx, data in enumerate(ALL_TEST_DATA, 1):
            cat_id = category_map[data["category"]]
            panel_id = panel_map[(data["category"], data["test_name"])]
            create_test_in_panel(
                db=db,
                category_id=cat_id,
                panel_id=panel_id,
                parameter=data["parameter"],
                normal_range=data["normal_range"],
                price=0.0
            )
            if idx % 50 == 0:  # progress indicator
                print(f"  ... processed {idx} tests")

        print("\n" + "-" * 80)
        print(f"All test data inserted/verified. Total records: {len(ALL_TEST_DATA)}")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()

# ============================================================
# 5. VERIFICATION / DISPLAY
# ============================================================
def list_inserted_data():
    db = SessionLocal()
    try:
        print("\n" + "=" * 80)
        print("VERIFICATION OF INSERTED DATA")
        print("=" * 80)

        panels = db.query(Panel).order_by(Panel.name).all()
        for panel in panels:
            tests = panel.tests
            print(f"\n[Panel] {panel.name} ({len(tests)} tests)")
            for item in tests:
                print(f"       - {item.name}: {item.reference_range}")
    except Exception as e:
        print(f"Verification error: {e}")
    finally:
        db.close()

# ============================================================
# 6. MAIN
# ============================================================
def main():
    print("=" * 80)
    print("LMS DATABASE SEEDING")
    print("=" * 80)

    # Ensure tables exist
    create_tables()

    # Seed admin
    seed_admin()

    # Seed tests
    seed_tests()

    # Show summary
    list_inserted_data()

    print("\nSeeding completed successfully!")

if __name__ == "__main__":
    main()