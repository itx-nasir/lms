#!/usr/bin/env python3
"""Run all test data insertion scripts (idempotent).
Each script lives in `scripts/insert_*.py` and handles its own checks.
"""
import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load .env so DB env vars are available when running the script
load_dotenv()

from importlib import import_module

# Diagnostic: print which DATABASE_URL / DB components will be used
print("[seed_tests] DATABASE_URL:", os.getenv('DATABASE_URL'))
print("[seed_tests] DB_HOST/PORT/USER/NAME:", os.getenv('DB_HOST'), os.getenv('DB_PORT'), os.getenv('DB_USER'), os.getenv('DB_NAME'))

INSERT_SCRIPTS = [
    'scripts.insert_biochemistry_data',
    'scripts.insert_haematology_data',
    'scripts.insert_immunology_serology_data',
    'scripts.insert_microbiology_parasitology_data',
    'scripts.insert_stool_data',
    'scripts.insert_urinalysis_data',
]

def run_inserts():
    for module_name in INSERT_SCRIPTS:
        print(f"Running {module_name}...")
        try:
            mod = import_module(module_name)
            # Each module exposes an `insert_*` function; call the one matching module
            # We use a simple convention: find a callable that contains 'insert' in its name
            for attr in dir(mod):
                if callable(getattr(mod, attr)) and 'insert' in attr:
                    func = getattr(mod, attr)
                    print(f"  - Calling {attr}()")
                    func()
                    break
        except Exception as e:
            print(f"Error running {module_name}: {e}")

if __name__ == '__main__':
    run_inserts()
