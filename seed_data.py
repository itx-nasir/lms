from database import SessionLocal, create_tables
import crud
import schemas

def seed():
    # Ensure tables exist (in case migrations not yet applied)
    create_tables()

    db = SessionLocal()
    try:
        # Create admin user if not exists
        admin = crud.get_admin_user(db, "admin")
        if not admin:
            crud.create_admin_user(db, "admin", "admin123")
            print("Created admin user: admin / admin123")
        else:
            print("Admin user already exists")

        # Create sample categories and tests
        if not crud.get_test_categories(db):
            cat1 = crud.create_test_category(db, schemas.TestCategoryCreate(name="Biochemistry"))
        else:
            cat1 = crud.get_test_categories(db)[0]

        # Add a sample test if none exist
        if not crud.get_tests(db):
            sample_test = crud.create_test(db, schemas.TestCreate(
                name="Glucose",
                price=50.0,
                unit="mg/dL",
                reference_range="70-110",
                category_id=cat1.id
            ))
            print("Created sample test: Glucose")
        else:
            print("Tests already present")

    finally:
        db.close()

if __name__ == '__main__':
    seed()
