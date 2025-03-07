"""prompt versioing

Revision ID: 822d89321fa5
Revises: 7fc4080dd744
Create Date: 2025-01-17 02:46:01.457709

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '822d89321fa5'
down_revision: Union[str, None] = '7fc4080dd744'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('prompt_store', sa.Column('prompt_type', sa.String(), nullable=False))
    op.add_column('prompt_store', sa.Column('prompt', sa.String(), nullable=False))
    op.add_column('questions', sa.Column('prompt_id', sa.UUID(), nullable=True))
    op.create_foreign_key(None, 'questions', 'prompt_store', ['prompt_id'], ['prompt_id'])
    op.add_column('reviews', sa.Column('prompt_id', sa.UUID(), nullable=True))
    op.create_foreign_key(None, 'reviews', 'prompt_store', ['prompt_id'], ['prompt_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'reviews', type_='foreignkey')
    op.drop_column('reviews', 'prompt_id')
    op.drop_constraint(None, 'questions', type_='foreignkey')
    op.drop_column('questions', 'prompt_id')
    op.drop_column('prompt_store', 'prompt')
    op.drop_column('prompt_store', 'prompt_type')
    # ### end Alembic commands ###
