"""Initial migration

Revision ID: 001_initial_migration
Revises: 
Create Date: 2026-02-09 10:00:00

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
import uuid

# revision identifiers, used by Alembic.
revision = '001_initial_migration'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table('user',
        sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    
    # Create tasks table
    op.create_table('task',
        sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column('user_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.String(length=1000), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create conversations table
    op.create_table('conversation',
        sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column('user_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create messages table
    op.create_table('message',
        sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column('conversation_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column('user_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column('role', sa.Enum('user', 'assistant', name='role'), nullable=False),
        sa.Column('content', sa.String(length=5000), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversation.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    # Drop messages table
    op.drop_table('message')
    
    # Drop conversations table
    op.drop_table('conversation')
    
    # Drop tasks table
    op.drop_table('task')
    
    # Drop users table
    op.drop_table('user')
    
    # Drop the enum type
    op.execute("DROP TYPE IF EXISTS role;")