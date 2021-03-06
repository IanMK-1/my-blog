"""Change column for writer/blog relstionship

Revision ID: 462e88986d6a
Revises: 452674ecb94f
Create Date: 2020-02-16 15:56:15.995880

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '462e88986d6a'
down_revision = '452674ecb94f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('blogs_writer_blog_fkey', 'blogs', type_='foreignkey')
    op.drop_column('blogs', 'writer_blog')
    op.add_column('writers', sa.Column('blog', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'writers', 'blogs', ['blog'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'writers', type_='foreignkey')
    op.drop_column('writers', 'blog')
    op.add_column('blogs', sa.Column('writer_blog', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('blogs_writer_blog_fkey', 'blogs', 'writers', ['writer_blog'], ['id'])
    # ### end Alembic commands ###
