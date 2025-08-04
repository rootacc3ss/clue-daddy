"""
Database migration management system.
"""

import sqlite3
import logging
from pathlib import Path
from typing import List, Dict, Any


class MigrationManager:
    """Manages database schema migrations."""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        
    def get_current_version(self) -> int:
        """Get current database schema version."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if migrations table exists
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name='migrations'
                """)
                
                if not cursor.fetchone():
                    return 0
                    
                # Get latest migration version
                cursor.execute("SELECT MAX(version) FROM migrations")
                result = cursor.fetchone()
                return result[0] if result[0] is not None else 0
                
        except Exception as e:
            self.logger.error(f"Error getting database version: {e}")
            return 0
            
    def create_migrations_table(self, conn: sqlite3.Connection):
        """Create migrations tracking table."""
        conn.execute("""
            CREATE TABLE IF NOT EXISTS migrations (
                version INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
    def apply_migrations(self) -> bool:
        """Apply all pending migrations."""
        try:
            current_version = self.get_current_version()
            migrations = self.get_migrations()
            
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("PRAGMA foreign_keys = ON")
                self.create_migrations_table(conn)
                
                for version, name, sql in migrations:
                    if version > current_version:
                        self.logger.info(f"Applying migration {version}: {name}")
                        
                        # Execute migration SQL
                        conn.executescript(sql)
                        
                        # Record migration
                        conn.execute(
                            "INSERT INTO migrations (version, name) VALUES (?, ?)",
                            (version, name)
                        )
                        
                conn.commit()
                
            self.logger.info("All migrations applied successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error applying migrations: {e}")
            return False
            
    def get_migrations(self) -> List[tuple]:
        """Get list of all migrations in order."""
        return [
            (1, "initial_schema", self.get_initial_schema()),
            (2, "add_indexes", self.get_indexes_migration()),
            (3, "add_perplexity_research", self.get_perplexity_research_migration()),
        ]
        
    def get_initial_schema(self) -> str:
        """Get initial database schema."""
        return """
        -- Configuration table
        CREATE TABLE IF NOT EXISTS config (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Profiles table
        CREATE TABLE IF NOT EXISTS profiles (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            profile_type TEXT NOT NULL,
            description TEXT,
            purpose TEXT,
            behavior_instructions TEXT,
            additional_context TEXT,
            custom_system_prompt TEXT,
            accent_color TEXT DEFAULT '#00BCD4',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Profile files table
        CREATE TABLE IF NOT EXISTS profile_files (
            id TEXT PRIMARY KEY,
            profile_id TEXT NOT NULL,
            filename TEXT NOT NULL,
            file_path TEXT NOT NULL,
            mime_type TEXT NOT NULL,
            extracted_text TEXT,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (profile_id) REFERENCES profiles (id) ON DELETE CASCADE
        );

        -- Sessions table
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            profile_id TEXT,
            title TEXT NOT NULL,
            start_time TIMESTAMP NOT NULL,
            end_time TIMESTAMP,
            duration_seconds INTEGER,
            tags TEXT, -- JSON array
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (profile_id) REFERENCES profiles (id) ON DELETE SET NULL
        );

        -- Session interactions table
        CREATE TABLE IF NOT EXISTS session_interactions (
            id TEXT PRIMARY KEY,
            session_id TEXT NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            interaction_type TEXT NOT NULL,
            content TEXT NOT NULL,
            ai_response TEXT NOT NULL,
            screenshot_path TEXT,
            audio_path TEXT,
            FOREIGN KEY (session_id) REFERENCES sessions (id) ON DELETE CASCADE
        );
        """
        
    def get_indexes_migration(self) -> str:
        """Get indexes migration."""
        return """
        -- Indexes for better performance
        CREATE INDEX IF NOT EXISTS idx_profiles_type ON profiles(profile_type);
        CREATE INDEX IF NOT EXISTS idx_profiles_created ON profiles(created_at);
        CREATE INDEX IF NOT EXISTS idx_profile_files_profile_id ON profile_files(profile_id);
        CREATE INDEX IF NOT EXISTS idx_sessions_profile_id ON sessions(profile_id);
        CREATE INDEX IF NOT EXISTS idx_sessions_start_time ON sessions(start_time);
        CREATE INDEX IF NOT EXISTS idx_session_interactions_session_id ON session_interactions(session_id);
        CREATE INDEX IF NOT EXISTS idx_session_interactions_timestamp ON session_interactions(timestamp);
        CREATE INDEX IF NOT EXISTS idx_session_interactions_type ON session_interactions(interaction_type);
        """
        
    def get_perplexity_research_migration(self) -> str:
        """Get Perplexity research table migration."""
        return """
        -- Perplexity research table
        CREATE TABLE IF NOT EXISTS perplexity_research (
            id TEXT PRIMARY KEY,
            profile_id TEXT NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            sources TEXT, -- JSON array of source URLs
            conducted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            appended_to_context BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (profile_id) REFERENCES profiles (id) ON DELETE CASCADE
        );
        
        -- Index for Perplexity research
        CREATE INDEX IF NOT EXISTS idx_perplexity_research_profile_id ON perplexity_research(profile_id);
        CREATE INDEX IF NOT EXISTS idx_perplexity_research_conducted_at ON perplexity_research(conducted_at);
        """