"""
Database connection management and CRUD operations.
"""

import sqlite3
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any
from contextlib import contextmanager
import threading
from datetime import datetime

from .models import Profile, Session, SessionInteraction, ProfileFile, PerplexityResearch
from .migrations import MigrationManager


class DatabaseManager:
    """Manages database connections and operations."""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self._local = threading.local()
        
        # Ensure database directory exists
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize database
        self._initialize_database()
        
    def _initialize_database(self):
        """Initialize database with schema migrations."""
        try:
            migration_manager = MigrationManager(self.db_path)
            success = migration_manager.apply_migrations()
            
            if success:
                self.logger.info("Database initialized successfully")
            else:
                self.logger.error("Failed to initialize database")
                
        except Exception as e:
            self.logger.error(f"Error initializing database: {e}")
            raise
            
    @contextmanager
    def get_connection(self):
        """Get database connection with proper cleanup."""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path, timeout=30.0)
            conn.execute("PRAGMA foreign_keys = ON")
            conn.execute("PRAGMA journal_mode = WAL")
            conn.row_factory = sqlite3.Row
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            self.logger.error(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()
                
    # Profile CRUD Operations
    
    def create_profile(self, profile: Profile) -> bool:
        """Create a new profile."""
        try:
            with self.get_connection() as conn:
                profile.updated_at = datetime.now()
                data = profile.to_dict()
                
                conn.execute("""
                    INSERT INTO profiles (
                        id, name, profile_type, description, purpose,
                        behavior_instructions, additional_context, custom_system_prompt,
                        accent_color, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    data["id"], data["name"], data["profile_type"], data["description"],
                    data["purpose"], data["behavior_instructions"], data["additional_context"],
                    data["custom_system_prompt"], data["accent_color"], 
                    data["created_at"], data["updated_at"]
                ))
                
                conn.commit()
                self.logger.info(f"Created profile: {profile.name}")
                return True
                
        except Exception as e:
            self.logger.error(f"Error creating profile: {e}")
            return False
            
    def get_profile(self, profile_id: str) -> Optional[Profile]:
        """Get profile by ID."""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("SELECT * FROM profiles WHERE id = ?", (profile_id,))
                row = cursor.fetchone()
                
                if row:
                    return Profile.from_dict(dict(row))
                return None
                
        except Exception as e:
            self.logger.error(f"Error getting profile: {e}")
            return None
            
    def get_all_profiles(self) -> List[Profile]:
        """Get all profiles."""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("SELECT * FROM profiles ORDER BY created_at DESC")
                rows = cursor.fetchall()
                
                return [Profile.from_dict(dict(row)) for row in rows]
                
        except Exception as e:
            self.logger.error(f"Error getting profiles: {e}")
            return []
            
    def update_profile(self, profile: Profile) -> bool:
        """Update existing profile."""
        try:
            with self.get_connection() as conn:
                profile.updated_at = datetime.now()
                data = profile.to_dict()
                
                conn.execute("""
                    UPDATE profiles SET
                        name = ?, profile_type = ?, description = ?, purpose = ?,
                        behavior_instructions = ?, additional_context = ?, 
                        custom_system_prompt = ?, accent_color = ?, updated_at = ?
                    WHERE id = ?
                """, (
                    data["name"], data["profile_type"], data["description"], data["purpose"],
                    data["behavior_instructions"], data["additional_context"],
                    data["custom_system_prompt"], data["accent_color"], 
                    data["updated_at"], data["id"]
                ))
                
                conn.commit()
                self.logger.info(f"Updated profile: {profile.name}")
                return True
                
        except Exception as e:
            self.logger.error(f"Error updating profile: {e}")
            return False
            
    def delete_profile(self, profile_id: str) -> bool:
        """Delete profile and associated files."""
        try:
            with self.get_connection() as conn:
                # Delete profile (cascade will handle files)
                conn.execute("DELETE FROM profiles WHERE id = ?", (profile_id,))
                conn.commit()
                
                self.logger.info(f"Deleted profile: {profile_id}")
                return True
                
        except Exception as e:
            self.logger.error(f"Error deleting profile: {e}")
            return False
            
    # Profile File CRUD Operations
    
    def create_profile_file(self, profile_file: ProfileFile) -> bool:
        """Create a new profile file."""
        try:
            with self.get_connection() as conn:
                data = profile_file.to_dict()
                
                conn.execute("""
                    INSERT INTO profile_files (
                        id, profile_id, filename, file_path, mime_type,
                        extracted_text, uploaded_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    data["id"], data["profile_id"], data["filename"], data["file_path"],
                    data["mime_type"], data["extracted_text"], data["uploaded_at"]
                ))
                
                conn.commit()
                self.logger.info(f"Created profile file: {profile_file.filename}")
                return True
                
        except Exception as e:
            self.logger.error(f"Error creating profile file: {e}")
            return False
            
    def get_profile_files(self, profile_id: str) -> List[ProfileFile]:
        """Get all files for a profile."""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(
                    "SELECT * FROM profile_files WHERE profile_id = ? ORDER BY uploaded_at DESC",
                    (profile_id,)
                )
                rows = cursor.fetchall()
                
                return [ProfileFile.from_dict(dict(row)) for row in rows]
                
        except Exception as e:
            self.logger.error(f"Error getting profile files: {e}")
            return []
            
    def delete_profile_file(self, file_id: str) -> bool:
        """Delete a profile file."""
        try:
            with self.get_connection() as conn:
                conn.execute("DELETE FROM profile_files WHERE id = ?", (file_id,))
                conn.commit()
                
                self.logger.info(f"Deleted profile file: {file_id}")
                return True
                
        except Exception as e:
            self.logger.error(f"Error deleting profile file: {e}")
            return False
            
    # Perplexity Research CRUD Operations
    
    def create_perplexity_research(self, research: PerplexityResearch) -> bool:
        """Create a new Perplexity research entry."""
        try:
            with self.get_connection() as conn:
                data = research.to_dict()
                
                conn.execute("""
                    INSERT INTO perplexity_research (
                        id, profile_id, question, answer, sources,
                        conducted_at, appended_to_context
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    data["id"], data["profile_id"], data["question"], data["answer"],
                    data["sources"], data["conducted_at"], data["appended_to_context"]
                ))
                
                conn.commit()
                self.logger.info(f"Created Perplexity research: {research.question[:50]}...")
                return True
                
        except Exception as e:
            self.logger.error(f"Error creating Perplexity research: {e}")
            return False
            
    def get_profile_research(self, profile_id: str) -> List[PerplexityResearch]:
        """Get all Perplexity research for a profile."""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(
                    "SELECT * FROM perplexity_research WHERE profile_id = ? ORDER BY conducted_at DESC",
                    (profile_id,)
                )
                rows = cursor.fetchall()
                
                return [PerplexityResearch.from_dict(dict(row)) for row in rows]
                
        except Exception as e:
            self.logger.error(f"Error getting profile research: {e}")
            return []
            
    def update_research_appended_status(self, research_id: str, appended: bool) -> bool:
        """Update whether research has been appended to context."""
        try:
            with self.get_connection() as conn:
                conn.execute(
                    "UPDATE perplexity_research SET appended_to_context = ? WHERE id = ?",
                    (appended, research_id)
                )
                conn.commit()
                return True
                
        except Exception as e:
            self.logger.error(f"Error updating research appended status: {e}")
            return False
            
    def delete_perplexity_research(self, research_id: str) -> bool:
        """Delete a Perplexity research entry."""
        try:
            with self.get_connection() as conn:
                conn.execute("DELETE FROM perplexity_research WHERE id = ?", (research_id,))
                conn.commit()
                
                self.logger.info(f"Deleted Perplexity research: {research_id}")
                return True
                
        except Exception as e:
            self.logger.error(f"Error deleting Perplexity research: {e}")
            return False
            
    # Session CRUD Operations
    
    def create_session(self, session: Session) -> bool:
        """Create a new session."""
        try:
            with self.get_connection() as conn:
                data = session.to_dict()
                
                conn.execute("""
                    INSERT INTO sessions (
                        id, profile_id, title, start_time, end_time,
                        duration_seconds, tags, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                """, (
                    data["id"], data["profile_id"], data["title"], data["start_time"],
                    data["end_time"], data["duration_seconds"], data["tags"]
                ))
                
                conn.commit()
                self.logger.info(f"Created session: {session.title}")
                return True
                
        except Exception as e:
            self.logger.error(f"Error creating session: {e}")
            return False
            
    def get_session(self, session_id: str) -> Optional[Session]:
        """Get session by ID."""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("SELECT * FROM sessions WHERE id = ?", (session_id,))
                row = cursor.fetchone()
                
                if row:
                    return Session.from_dict(dict(row))
                return None
                
        except Exception as e:
            self.logger.error(f"Error getting session: {e}")
            return None
            
    def get_all_sessions(self, limit: Optional[int] = None) -> List[Session]:
        """Get all sessions, optionally limited."""
        try:
            with self.get_connection() as conn:
                query = "SELECT * FROM sessions ORDER BY start_time DESC"
                if limit:
                    query += f" LIMIT {limit}"
                    
                cursor = conn.execute(query)
                rows = cursor.fetchall()
                
                return [Session.from_dict(dict(row)) for row in rows]
                
        except Exception as e:
            self.logger.error(f"Error getting sessions: {e}")
            return []
            
    def update_session(self, session: Session) -> bool:
        """Update existing session."""
        try:
            with self.get_connection() as conn:
                data = session.to_dict()
                
                conn.execute("""
                    UPDATE sessions SET
                        title = ?, end_time = ?, duration_seconds = ?, tags = ?
                    WHERE id = ?
                """, (
                    data["title"], data["end_time"], data["duration_seconds"],
                    data["tags"], data["id"]
                ))
                
                conn.commit()
                self.logger.info(f"Updated session: {session.title}")
                return True
                
        except Exception as e:
            self.logger.error(f"Error updating session: {e}")
            return False
            
    def delete_session(self, session_id: str) -> bool:
        """Delete session and associated interactions."""
        try:
            with self.get_connection() as conn:
                # Delete session (cascade will handle interactions)
                conn.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
                conn.commit()
                
                self.logger.info(f"Deleted session: {session_id}")
                return True
                
        except Exception as e:
            self.logger.error(f"Error deleting session: {e}")
            return False
            
    # Session Interaction CRUD Operations
    
    def create_session_interaction(self, interaction: SessionInteraction) -> bool:
        """Create a new session interaction."""
        try:
            with self.get_connection() as conn:
                data = interaction.to_dict()
                
                conn.execute("""
                    INSERT INTO session_interactions (
                        id, session_id, timestamp, interaction_type, content,
                        ai_response, screenshot_path, audio_path
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    data["id"], data["session_id"], data["timestamp"], data["interaction_type"],
                    data["content"], data["ai_response"], data["screenshot_path"], data["audio_path"]
                ))
                
                conn.commit()
                return True
                
        except Exception as e:
            self.logger.error(f"Error creating session interaction: {e}")
            return False
            
    def get_session_interactions(self, session_id: str) -> List[SessionInteraction]:
        """Get all interactions for a session."""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(
                    "SELECT * FROM session_interactions WHERE session_id = ? ORDER BY timestamp ASC",
                    (session_id,)
                )
                rows = cursor.fetchall()
                
                return [SessionInteraction.from_dict(dict(row)) for row in rows]
                
        except Exception as e:
            self.logger.error(f"Error getting session interactions: {e}")
            return []
            
    # Utility Methods
    
    def get_database_info(self) -> Dict[str, Any]:
        """Get database information and statistics."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Get table counts
                cursor.execute("SELECT COUNT(*) FROM profiles")
                profile_count = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM sessions")
                session_count = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM session_interactions")
                interaction_count = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM profile_files")
                file_count = cursor.fetchone()[0]
                
                # Get research count (may not exist in older databases)
                try:
                    cursor.execute("SELECT COUNT(*) FROM perplexity_research")
                    research_count = cursor.fetchone()[0]
                except:
                    research_count = 0
                
                # Get database size
                db_size = Path(self.db_path).stat().st_size if Path(self.db_path).exists() else 0
                
                return {
                    "database_path": self.db_path,
                    "database_size_bytes": db_size,
                    "profile_count": profile_count,
                    "session_count": session_count,
                    "interaction_count": interaction_count,
                    "file_count": file_count,
                    "research_count": research_count,
                }
                
        except Exception as e:
            self.logger.error(f"Error getting database info: {e}")
            return {}
            
    def cleanup_old_sessions(self, days_old: int) -> int:
        """Clean up sessions older than specified days."""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("""
                    DELETE FROM sessions 
                    WHERE start_time < datetime('now', '-{} days')
                """.format(days_old))
                
                deleted_count = cursor.rowcount
                conn.commit()
                
                self.logger.info(f"Cleaned up {deleted_count} old sessions")
                return deleted_count
                
        except Exception as e:
            self.logger.error(f"Error cleaning up old sessions: {e}")
            return 0