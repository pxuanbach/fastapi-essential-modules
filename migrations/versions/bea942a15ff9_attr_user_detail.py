"""attr user detail

Revision ID: bea942a15ff9
Revises: 74e0c7445ce9
Create Date: 2024-07-25 14:01:41.135569

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel   


# revision identifiers, used by Alembic.
revision: str = 'bea942a15ff9'
down_revision: Union[str, None] = '74e0c7445ce9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('attrs',
    sa.Column('title', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_attrs_id'), 'attrs', ['id'], unique=False)
    op.create_table('user_attrs',
    sa.Column('user_id', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.Column('attr_id', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.ForeignKeyConstraint(['attr_id'], ['attrs.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_attrs_id'), 'user_attrs', ['id'], unique=False)
    op.create_table('user_details',
    sa.Column('user_id', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.Column('address', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_details_id'), 'user_details', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_details_id'), table_name='user_details')
    op.drop_table('user_details')
    op.drop_index(op.f('ix_user_attrs_id'), table_name='user_attrs')
    op.drop_table('user_attrs')
    op.drop_index(op.f('ix_attrs_id'), table_name='attrs')
    op.drop_table('attrs')
    # ### end Alembic commands ###