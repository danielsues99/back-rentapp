"""Initial migration

Revision ID: eea9b1e56f83
Revises: 
Create Date: 2024-08-19 18:05:29.393383

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eea9b1e56f83'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('landlord',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('address', sa.String(length=120), nullable=True),
    sa.Column('contract', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    with op.batch_alter_table('landlord', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_landlord_name'), ['name'], unique=False)

    op.create_table('tenant',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('property_address', sa.String(length=120), nullable=True),
    sa.Column('landlord_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['landlord_id'], ['landlord.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    with op.batch_alter_table('tenant', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_tenant_name'), ['name'], unique=False)

    op.create_table('payment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('due_date', sa.Date(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('tenant_id', sa.Integer(), nullable=True),
    sa.Column('payment_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['tenant_id'], ['tenant.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payment')
    with op.batch_alter_table('tenant', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_tenant_name'))

    op.drop_table('tenant')
    with op.batch_alter_table('landlord', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_landlord_name'))

    op.drop_table('landlord')
    # ### end Alembic commands ###
