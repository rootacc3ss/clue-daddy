"""
Data models for Clue Daddy database entities.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
import uuid
import json


@dataclass
class Profile:
    """Profile data model for context profiles."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    profile_type: str = "interview"  # interview, sales, meeting, presentation, negotiation, exam
    description: str = ""
    purpose: str = ""
    behavior_instructions: str = ""
    additional_context: str = ""
    custom_system_prompt: Optional[str] = None
    accent_color: str = "#00BCD4"
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for database storage."""
        return {
            "id": self.id,
            "name": self.name,
            "profile_type": self.profile_type,
            "description": self.description,
            "purpose": self.purpose,
            "behavior_instructions": self.behavior_instructions,
            "additional_context": self.additional_context,
            "custom_system_prompt": self.custom_system_prompt,
            "accent_color": self.accent_color,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Profile':
        """Create Profile from dictionary."""
        # Handle datetime fields
        created_at = datetime.fromisoformat(data.get("created_at", datetime.now().isoformat()))
        updated_at = datetime.fromisoformat(data.get("updated_at", datetime.now().isoformat()))
        
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            name=data.get("name", ""),
            profile_type=data.get("profile_type", "interview"),
            description=data.get("description", ""),
            purpose=data.get("purpose", ""),
            behavior_instructions=data.get("behavior_instructions", ""),
            additional_context=data.get("additional_context", ""),
            custom_system_prompt=data.get("custom_system_prompt"),
            accent_color=data.get("accent_color", "#00BCD4"),
            created_at=created_at,
            updated_at=updated_at,
        )


@dataclass
class ProfileFile:
    """Profile file data model."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    profile_id: str = ""
    filename: str = ""
    file_path: str = ""
    mime_type: str = ""
    extracted_text: Optional[str] = None
    uploaded_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for database storage."""
        return {
            "id": self.id,
            "profile_id": self.profile_id,
            "filename": self.filename,
            "file_path": self.file_path,
            "mime_type": self.mime_type,
            "extracted_text": self.extracted_text,
            "uploaded_at": self.uploaded_at.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ProfileFile':
        """Create ProfileFile from dictionary."""
        uploaded_at = datetime.fromisoformat(data.get("uploaded_at", datetime.now().isoformat()))
        
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            profile_id=data.get("profile_id", ""),
            filename=data.get("filename", ""),
            file_path=data.get("file_path", ""),
            mime_type=data.get("mime_type", ""),
            extracted_text=data.get("extracted_text"),
            uploaded_at=uploaded_at,
        )


@dataclass
class Session:
    """Session data model."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    profile_id: Optional[str] = None
    title: str = ""
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for database storage."""
        return {
            "id": self.id,
            "profile_id": self.profile_id,
            "title": self.title,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_seconds": self.duration_seconds,
            "tags": json.dumps(self.tags),
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Session':
        """Create Session from dictionary."""
        start_time = datetime.fromisoformat(data.get("start_time", datetime.now().isoformat()))
        end_time = None
        if data.get("end_time"):
            end_time = datetime.fromisoformat(data["end_time"])
            
        tags = []
        if data.get("tags"):
            try:
                tags = json.loads(data["tags"])
            except (json.JSONDecodeError, TypeError):
                tags = []
        
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            profile_id=data.get("profile_id"),
            title=data.get("title", ""),
            start_time=start_time,
            end_time=end_time,
            duration_seconds=data.get("duration_seconds"),
            tags=tags,
        )
    
    def calculate_duration(self) -> Optional[int]:
        """Calculate session duration in seconds."""
        if self.end_time and self.start_time:
            delta = self.end_time - self.start_time
            return int(delta.total_seconds())
        return None
    
    def finalize(self):
        """Finalize the session by setting end time and calculating duration."""
        self.end_time = datetime.now()
        self.duration_seconds = self.calculate_duration()


@dataclass
class SessionInteraction:
    """Session interaction data model."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    interaction_type: str = "voice"  # voice, user_prompt
    content: str = ""  # Transcript or user message
    ai_response: str = ""
    screenshot_path: Optional[str] = None
    audio_path: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary for database storage."""
        return {
            "id": self.id,
            "session_id": self.session_id,
            "timestamp": self.timestamp.isoformat(),
            "interaction_type": self.interaction_type,
            "content": self.content,
            "ai_response": self.ai_response,
            "screenshot_path": self.screenshot_path,
            "audio_path": self.audio_path,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'SessionInteraction':
        """Create SessionInteraction from dictionary."""
        timestamp = datetime.fromisoformat(data.get("timestamp", datetime.now().isoformat()))
        
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            session_id=data.get("session_id", ""),
            timestamp=timestamp,
            interaction_type=data.get("interaction_type", "voice"),
            content=data.get("content", ""),
            ai_response=data.get("ai_response", ""),
            screenshot_path=data.get("screenshot_path"),
            audio_path=data.get("audio_path"),
        )


@dataclass
class PerplexityResearch:
    """Perplexity research data model."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    profile_id: str = ""
    question: str = ""
    answer: str = ""
    sources: List[str] = field(default_factory=list)
    conducted_at: datetime = field(default_factory=datetime.now)
    appended_to_context: bool = False
    
    def to_dict(self) -> dict:
        """Convert to dictionary for database storage."""
        return {
            "id": self.id,
            "profile_id": self.profile_id,
            "question": self.question,
            "answer": self.answer,
            "sources": json.dumps(self.sources),
            "conducted_at": self.conducted_at.isoformat(),
            "appended_to_context": self.appended_to_context,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'PerplexityResearch':
        """Create PerplexityResearch from dictionary."""
        conducted_at = datetime.fromisoformat(data.get("conducted_at", datetime.now().isoformat()))
        
        sources = []
        if data.get("sources"):
            try:
                sources = json.loads(data["sources"])
            except (json.JSONDecodeError, TypeError):
                sources = []
        
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            profile_id=data.get("profile_id", ""),
            question=data.get("question", ""),
            answer=data.get("answer", ""),
            sources=sources,
            conducted_at=conducted_at,
            appended_to_context=data.get("appended_to_context", False),
        )
    
    def format_for_context(self) -> str:
        """Format research result for inclusion in profile context."""
        sources_text = ""
        if self.sources:
            sources_text = f"\nSources: {', '.join(self.sources)}"
        
        return f"**RESEARCH: {self.question}**\n{self.answer}{sources_text}"