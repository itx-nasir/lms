#!/usr/bin/env python3
"""
Seed the database with the admin user and the test catalog from test_data.json.
Safe to run repeatedly: existing categories, panels and tests are reused.

    python scripts/seed_data.py
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from main import init_db  # noqa: E402  (also creates tables + admin user)
from database import SessionLocal  # noqa: E402
from models import Panel, PanelTest, Test, TestCategory  # noqa: E402

DATA_FILE = os.path.join(ROOT, "test_data.json")
REQUIRED_FIELDS = {"category", "test_name", "parameter", "range", "unit"}


def load_test_data():
    with open(DATA_FILE, encoding="utf-8") as f:
        data = json.load(f)
    for idx, item in enumerate(data):
        missing = REQUIRED_FIELDS - item.keys()
        if missing:
            sys.exit(f"Item #{idx} in test_data.json is missing: {', '.join(sorted(missing))}")
    return data


def get_or_create(db, model, **fields):
    obj = db.query(model).filter_by(**fields).first()
    if not obj:
        obj = model(**fields)
        db.add(obj)
        db.flush()
    return obj


def seed_tests(db, data):
    # Generic group names (e.g. "Physical Examination") appear in several
    # categories; each occurrence becomes its own panel, suffixed with the category.
    group_categories = {}
    for item in data:
        group_categories.setdefault(item["test_name"], set()).add(item["category"])

    created = 0
    for item in data:
        category = get_or_create(db, TestCategory, name=item["category"])
        panel_name = item["test_name"]
        if len(group_categories[panel_name]) > 1:
            panel_name = f"{panel_name} ({item['category'].split('/')[0].split(' ')[0]})"
        panel = db.query(Panel).filter_by(name=panel_name).first()
        if not panel:
            panel = Panel(name=panel_name, price=0.0)
            db.add(panel)
            db.flush()

        exists = (
            db.query(Test).join(PanelTest, PanelTest.test_id == Test.id)
            .filter(PanelTest.panel_id == panel.id, Test.name == item["parameter"])
            .first()
        )
        if exists:
            continue
        test = Test(
            name=item["parameter"], price=0.0, category_id=category.id,
            reference_range=item["range"], unit=item["unit"],
        )
        db.add(test)
        db.flush()
        db.add(PanelTest(panel_id=panel.id, test_id=test.id, sequence=len(panel.panel_tests)))
        db.flush()
        db.expire(panel, ["panel_tests"])
        created += 1

    db.commit()
    return created


def main():
    data = load_test_data()
    init_db()
    with SessionLocal() as db:
        created = seed_tests(db, data)
    print(f"Loaded {len(data)} records from test_data.json; {created} new tests created.")


if __name__ == "__main__":
    main()
