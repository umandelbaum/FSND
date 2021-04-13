"""empty message

Revision ID: 3b4922d5dfe7
Revises: 
Create Date: 2021-04-12 21:39:05.030268

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b4922d5dfe7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('heroes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('secret_identity', sa.String(), nullable=True),
    sa.Column('hometown', sa.String(), nullable=True),
    sa.Column('power_level', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('teams',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('location', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('team_members',
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.Column('hero_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['hero_id'], ['heroes.id'], ),
    sa.ForeignKeyConstraint(['team_id'], ['teams.id'], ),
    sa.PrimaryKeyConstraint('team_id', 'hero_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('team_members')
    op.drop_table('teams')
    op.drop_table('heroes')
    # ### end Alembic commands ###
