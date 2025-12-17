#!/usr/bin/env python3
"""Convenience script to seed admin and all test data."""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from importlib import import_module

def run():
    print('Seeding admin...')
    import scripts.seed_admin as seed_admin
    seed_admin.seed_admin()

    print('\nSeeding tests...')
    import scripts.seed_tests as seed_tests
    seed_tests.run_inserts()

if __name__ == '__main__':
    run()
