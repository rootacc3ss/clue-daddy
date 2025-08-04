"""
Profile system prompt builder for combining universal prompt with profile data.
"""

from typing import List, Optional
from ..database.models import Profile, ProfileFile, PerplexityResearch


class ProfilePromptBuilder:
    """Builds comprehensive system prompts from profile data."""
    
    def __init__(self, universal_prompt: str):
        self.universal_prompt = universal_prompt
        
    def build_comprehensive_system_prompt(
        self, 
        profile: Profile, 
        profile_files: List[ProfileFile] = None,
        perplexity_research: List[PerplexityResearch] = None,
        personal_context: str = ""
    ) -> str:
        """
        Build complete system prompt combining universal prompt with all profile data.
        
        Args:
            profile: The profile containing purpose, behavior, and context
            profile_files: List of files associated with the profile
            perplexity_research: List of research conducted for the profile
            personal_context: User's personal context from settings
            
        Returns:
            Complete system prompt ready for AI
        """
        context_sections = []
        
        # Start with universal system prompt
        context_sections.append(self.universal_prompt)
        
        # Add personal context if provided
        if personal_context.strip():
            context_sections.append(f"**PERSONAL CONTEXT:**\n{personal_context.strip()}")
        
        # Add profile-specific sections
        if profile.purpose.strip():
            context_sections.append(f"**PROFILE PURPOSE:**\n{profile.purpose.strip()}")
        
        if profile.behavior_instructions.strip():
            context_sections.append(f"**BEHAVIOR INSTRUCTIONS:**\n{profile.behavior_instructions.strip()}")
        
        if profile.additional_context.strip():
            context_sections.append(f"**ADDITIONAL CONTEXT:**\n{profile.additional_context.strip()}")
        
        # Add file contents
        if profile_files:
            file_contents = []
            for file in profile_files:
                if file.extracted_text and file.extracted_text.strip():
                    file_contents.append(f"**FILE: {file.filename}**\n{file.extracted_text.strip()}")
            
            if file_contents:
                context_sections.append("**UPLOADED FILES:**\n" + "\n\n".join(file_contents))
        
        # Add Perplexity research
        if perplexity_research:
            research_contents = []
            for research in perplexity_research:
                if research.answer.strip():
                    sources_text = ""
                    if research.sources:
                        sources_text = f"\nSources: {', '.join(research.sources)}"
                    
                    research_contents.append(
                        f"**RESEARCH: {research.question}**\n{research.answer.strip()}{sources_text}"
                    )
            
            if research_contents:
                context_sections.append("**RESEARCH FINDINGS:**\n" + "\n\n".join(research_contents))
        
        # Add custom system prompt override if specified
        if profile.custom_system_prompt and profile.custom_system_prompt.strip():
            context_sections.append(f"**CUSTOM INSTRUCTIONS:**\n{profile.custom_system_prompt.strip()}")
        
        # Combine all sections
        full_prompt = "\n\n".join(context_sections)
        
        # Always end with the ready message instruction
        if not full_prompt.endswith("I'm ready to help!"):
            full_prompt += "\n\nI'm ready to help!"
        
        return full_prompt
    
    def build_basic_prompt(self, personal_context: str = "") -> str:
        """
        Build basic prompt with just universal prompt and personal context.
        Used when no profile is selected.
        
        Args:
            personal_context: User's personal context from settings
            
        Returns:
            Basic system prompt
        """
        if personal_context.strip():
            prompt = f"{self.universal_prompt}\n\n**PERSONAL CONTEXT:**\n{personal_context.strip()}"
        else:
            prompt = self.universal_prompt
            
        if not prompt.endswith("I'm ready to help!"):
            prompt += "\n\nI'm ready to help!"
            
        return prompt
    
    def preview_prompt_structure(self, profile: Profile) -> dict:
        """
        Preview what sections would be included in the prompt.
        Useful for UI display.
        
        Args:
            profile: The profile to preview
            
        Returns:
            Dictionary with section information
        """
        sections = {
            "universal_prompt": True,
            "personal_context": False,  # Would need to be passed in
            "profile_purpose": bool(profile.purpose.strip()),
            "behavior_instructions": bool(profile.behavior_instructions.strip()),
            "additional_context": bool(profile.additional_context.strip()),
            "uploaded_files": False,  # Would need files to be passed in
            "research_findings": False,  # Would need research to be passed in
            "custom_instructions": bool(profile.custom_system_prompt and profile.custom_system_prompt.strip()),
        }
        
        return sections
    
    def estimate_prompt_length(
        self, 
        profile: Profile, 
        profile_files: List[ProfileFile] = None,
        perplexity_research: List[PerplexityResearch] = None,
        personal_context: str = ""
    ) -> int:
        """
        Estimate the total length of the generated prompt.
        Useful for token counting and validation.
        
        Returns:
            Estimated character count
        """
        # This is a rough estimate - actual prompt would need to be built for exact count
        total_length = len(self.universal_prompt)
        
        if personal_context:
            total_length += len(personal_context) + 30  # +30 for header
            
        if profile.purpose:
            total_length += len(profile.purpose) + 25
            
        if profile.behavior_instructions:
            total_length += len(profile.behavior_instructions) + 35
            
        if profile.additional_context:
            total_length += len(profile.additional_context) + 30
            
        if profile_files:
            for file in profile_files:
                if file.extracted_text:
                    total_length += len(file.extracted_text) + len(file.filename) + 20
                    
        if perplexity_research:
            for research in perplexity_research:
                total_length += len(research.question) + len(research.answer) + 30
                if research.sources:
                    total_length += sum(len(source) for source in research.sources) + 20
                    
        if profile.custom_system_prompt:
            total_length += len(profile.custom_system_prompt) + 35
            
        total_length += 25  # For "I'm ready to help!" and spacing
        
        return total_length