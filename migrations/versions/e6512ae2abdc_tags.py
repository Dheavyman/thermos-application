"""tags

Revision ID: e6512ae2abdc
Revises: 1ad23548460a
Create Date: 2018-04-11 15:04:26.213039

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6512ae2abdc'
down_revision = '1ad23548460a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=25), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tag_name'), 'tag', ['name'], unique=True)
    op.create_table('bookmark_tag',
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.Column('bookmark_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['bookmark_id'], ['bookmark.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], )
    )
    op.alter_column('user', 'password_harsh',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'password_harsh',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_table('bookmark_tag')
    op.drop_index(op.f('ix_tag_name'), table_name='tag')
    op.drop_table('tag')
    # ### end Alembic commands ###
