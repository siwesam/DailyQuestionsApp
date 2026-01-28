"""
Database migration to add AI-related fields to quotes table.
This migration preserves existing data.
"""
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import sys
import os

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import settings
from app.database import Base, engine


def upgrade():
    """Add new columns to quotes table."""
    print("Starting migration: Adding AI-related fields to quotes table...")
    
    with engine.connect() as conn:
        # Detect database type
        db_url = str(engine.url)
        is_sqlite = 'sqlite' in db_url
        
        if is_sqlite:
            # SQLite: Try to add columns, ignore if they exist
            print("Detected SQLite database")
            
            try:
                print("Adding 'source' column...")
                conn.execute(text("ALTER TABLE quotes ADD COLUMN source VARCHAR(255)"))
                conn.commit()
                print("✓ Added 'source' column")
            except Exception as e:
                if "duplicate column" in str(e).lower():
                    print("✓ 'source' column already exists")
                else:
                    raise
            
            try:
                print("Adding 'is_ai_generated' column...")
                conn.execute(text("ALTER TABLE quotes ADD COLUMN is_ai_generated INTEGER DEFAULT 0"))
                conn.commit()
                print("✓ Added 'is_ai_generated' column")
            except Exception as e:
                if "duplicate column" in str(e).lower():
                    print("✓ 'is_ai_generated' column already exists")
                else:
                    raise
            
            try:
                print("Adding 'ai_relevance_reason' column...")
                conn.execute(text("ALTER TABLE quotes ADD COLUMN ai_relevance_reason TEXT"))
                conn.commit()
                print("✓ Added 'ai_relevance_reason' column")
            except Exception as e:
                if "duplicate column" in str(e).lower():
                    print("✓ 'ai_relevance_reason' column already exists")
                else:
                    raise
        else:
            # PostgreSQL: Check if columns exist first
            print("Detected PostgreSQL database")
            
            result = conn.execute(text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name='quotes' AND column_name='source'
            """))
            
            if result.fetchone() is None:
                print("Adding 'source' column...")
                conn.execute(text("ALTER TABLE quotes ADD COLUMN source VARCHAR(255)"))
                conn.commit()
                print("✓ Added 'source' column")
            else:
                print("✓ 'source' column already exists")
            
            result = conn.execute(text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name='quotes' AND column_name='is_ai_generated'
            """))
            
            if result.fetchone() is None:
                print("Adding 'is_ai_generated' column...")
                conn.execute(text("ALTER TABLE quotes ADD COLUMN is_ai_generated INTEGER DEFAULT 0"))
                conn.commit()
                print("✓ Added 'is_ai_generated' column")
            else:
                print("✓ 'is_ai_generated' column already exists")
            
            result = conn.execute(text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name='quotes' AND column_name='ai_relevance_reason'
            """))
            
            if result.fetchone() is None:
                print("Adding 'ai_relevance_reason' column...")
                conn.execute(text("ALTER TABLE quotes ADD COLUMN ai_relevance_reason TEXT"))
                conn.commit()
                print("✓ Added 'ai_relevance_reason' column")
            else:
                print("✓ 'ai_relevance_reason' column already exists")
        
        # Update existing quotes to mark them as manually added
        print("Updating existing quotes...")
        conn.execute(text("""
            UPDATE quotes
            SET source = 'manual', is_ai_generated = 0
            WHERE source IS NULL
        """))
        conn.commit()
        print("✓ Updated existing quotes")
    
    print("Migration completed successfully!")


def downgrade():
    """Remove the added columns (use with caution)."""
    print("Starting rollback: Removing AI-related fields from quotes table...")
    
    with engine.connect() as conn:
        print("Removing 'ai_relevance_reason' column...")
        conn.execute(text("ALTER TABLE quotes DROP COLUMN IF EXISTS ai_relevance_reason"))
        conn.commit()
        
        print("Removing 'is_ai_generated' column...")
        conn.execute(text("ALTER TABLE quotes DROP COLUMN IF EXISTS is_ai_generated"))
        conn.commit()
        
        print("Removing 'source' column...")
        conn.execute(text("ALTER TABLE quotes DROP COLUMN IF EXISTS source"))
        conn.commit()
    
    print("Rollback completed!")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Database migration for AI quote fields')
    parser.add_argument('--downgrade', action='store_true', help='Rollback the migration')
    args = parser.parse_args()
    
    if args.downgrade:
        confirm = input("Are you sure you want to rollback? This will remove columns. (yes/no): ")
        if confirm.lower() == 'yes':
            downgrade()
        else:
            print("Rollback cancelled.")
    else:
        upgrade()

# Made with Bob