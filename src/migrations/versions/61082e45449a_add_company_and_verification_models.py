"""add company and verification models

Revision ID: 61082e45449a
Revises: 49abb5ecf31a
Create Date: 2026-07-11 11:04:34.176880

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '61082e45449a'
down_revision: Union[str, Sequence[str], None] = '49abb5ecf31a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # legal_docs (and its status enum) must go first: the new 'verifications'
    # table reuses the 'docverificationstatus' type name with a different set
    # of values, and Postgres enum types are global, not per-table.
    op.drop_table('legal_docs')
    op.execute('DROP TYPE docverificationstatus')

    op.create_table('companies',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('inn', sa.String(length=12), nullable=False),
    sa.Column('ogrn', sa.String(length=15), nullable=True),
    sa.Column('company_name', sa.String(length=255), nullable=True),
    sa.Column('region', sa.String(length=3), nullable=True),
    sa.Column('kpp', sa.String(length=9), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('inn')
    )
    op.create_table('verifications',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('type', sa.Enum('EGRUL', 'FSSP', 'BANKRUPTCY', name='verificationtype'), nullable=False),
    sa.Column('provider', sa.String(length=50), nullable=True),
    sa.Column('external_ref', sa.String(length=255), nullable=True),
    sa.Column('status', sa.Enum('PENDING', 'VERIFIED', 'FLAGGED', 'FAILED', name='docverificationstatus'), server_default=sa.text("'PENDING'"), nullable=False),
    sa.Column('result_json', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('checked_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('company_id', 'type', name='uq_verification_company_type')
    )
    op.add_column('forms', sa.Column('company_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'forms', 'companies', ['company_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, 'forms', type_='foreignkey')
    op.drop_column('forms', 'company_id')

    op.drop_table('verifications')
    op.drop_table('companies')
    op.execute('DROP TYPE docverificationstatus')
    op.execute('DROP TYPE verificationtype')

    op.create_table('legal_docs',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('form_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('status', postgresql.ENUM('PENDING', 'VERIFIED', 'REJECTED', name='docverificationstatus'), server_default=sa.text("'PENDING'::docverificationstatus"), autoincrement=False, nullable=False),
    sa.Column('filepath', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('uploaded_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text("timezone('utc'::text, now())"), autoincrement=False, nullable=False),
    sa.Column('processed_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['form_id'], ['forms.id'], name=op.f('legal_docs_form_id_fkey')),
    sa.PrimaryKeyConstraint('id', name=op.f('legal_docs_pkey'))
    )
    # ### end Alembic commands ###
