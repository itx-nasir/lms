"""create initial tables

Revision ID: 0001_create_initial_tables
Revises: 
Create Date: 2025-12-17 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_create_initial_tables'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'admin_users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('username', sa.String(length=50), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'patients',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('age', sa.Integer(), nullable=False),
        sa.Column('gender', sa.String(length=10), nullable=False),
        sa.Column('phone', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'test_categories',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=100), nullable=False),
    )

    op.create_table(
        'tests',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('unit', sa.String(length=20), nullable=True),
        sa.Column('reference_range', sa.String(length=100), nullable=True),
        sa.Column('category_id', sa.Integer(), sa.ForeignKey('test_categories.id'), nullable=False),
    )

    op.create_table(
        'test_orders',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('patient_id', sa.Integer(), sa.ForeignKey('patients.id'), nullable=False),
        sa.Column('ordered_at', sa.DateTime(), nullable=True),
        sa.Column('total_amount', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='pending'),
    )

    op.create_table(
        'test_order_items',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('order_id', sa.Integer(), sa.ForeignKey('test_orders.id'), nullable=False),
        sa.Column('test_id', sa.Integer(), sa.ForeignKey('tests.id'), nullable=False),
        sa.Column('result_value', sa.String(length=100), nullable=True),
        sa.Column('result_notes', sa.Text(), nullable=True),
    )


def downgrade():
    op.drop_table('test_order_items')
    op.drop_table('test_orders')
    op.drop_table('tests')
    op.drop_table('test_categories')
    op.drop_table('patients')
    op.drop_table('admin_users')
