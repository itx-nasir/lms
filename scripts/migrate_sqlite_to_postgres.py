#!/usr/bin/env python3
"""
Copy all data from an old desktop SQLite database into the Postgres database
in DATABASE_URL (e.g. Neon). The target must not contain any lab data yet;
admin users that already exist in the target are kept.

    python scripts/migrate_sqlite_to_postgres.py "%APPDATA%\\LMS\\lms.db"
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from sqlalchemy import create_engine, func, select, text  # noqa: E402

from database import engine as target_engine  # noqa: E402
from models import AdminUser, Base  # noqa: E402


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    source_path = os.path.expandvars(sys.argv[1])
    if not os.path.isfile(source_path):
        sys.exit(f"SQLite file not found: {source_path}")
    if target_engine.dialect.name != "postgresql":
        sys.exit("DATABASE_URL must point to the Postgres database to copy into.")

    source_engine = create_engine(f"sqlite:///{source_path}")
    Base.metadata.create_all(bind=target_engine)
    admin_table = AdminUser.__table__
    tables = [t for t in Base.metadata.sorted_tables if t is not admin_table]

    with source_engine.connect() as src, target_engine.begin() as dst:
        for table in tables:
            if dst.execute(select(func.count()).select_from(table)).scalar():
                sys.exit(f"Target table '{table.name}' already has data; aborting without changes.")

        existing_admins = set(dst.execute(select(admin_table.c.username)).scalars())
        admins = [
            {k: v for k, v in row._mapping.items() if k != "id"}
            for row in src.execute(admin_table.select())
            if row.username not in existing_admins
        ]
        if admins:
            dst.execute(admin_table.insert(), admins)
        print(f"admin_users: {len(admins)} copied")

        for table in tables:
            rows = [dict(row._mapping) for row in src.execute(table.select())]
            if rows:
                dst.execute(table.insert(), rows)
            # Explicit ids bypass the serial sequence, so move it past the copied rows.
            dst.execute(text(
                f"SELECT setval(pg_get_serial_sequence('{table.name}', 'id'), "
                f"COALESCE(MAX(id), 1), MAX(id) IS NOT NULL) FROM {table.name}"
            ))
            print(f"{table.name}: {len(rows)} copied")

    print("Done.")


if __name__ == "__main__":
    main()
