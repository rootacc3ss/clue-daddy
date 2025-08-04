"""
Perplexity API client for research functionality.
"""

import requests
import logging
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class PerplexityResult:
    """Result from Perplexity API research."""
    question: str
    answer: str
    sources: List[str]
    timestamp: datetime
    
    def format_for_context(self) -> str:
        """Format research result for inclusion in profile context."""
        sources_text = ""
        if self.sources:
            sources_text = f"\nSources: {', '.join(self.sources)}"
        
        return f"**RESEARCH: {self.question}**\n{self.answer}{sources_text}"


class PerplexityClient:
    """Client for interacting with Perplexity API."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.perplexity.ai"
        self.logger = logging.getLogger(__name__)
        
        # Headers for API requests
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
    
    def ask_question(self, question: str, model: str = "llama-3.1-sonar-small-128k-online") -> Optional[PerplexityResult]:
        """
        Ask a question to Perplexity and get an answer with sources.
        
        Args:
            question: The question to ask
            model: The model to use (default: llama-3.1-sonar-small-128k-online)
            
        Returns:
            PerplexityResult with answer and sources, or None if failed
        """
        try:
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "system",
                        "content": "Be precise and informative. Provide comprehensive answers with relevant sources."
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ],
                "max_tokens": 1000,
                "temperature": 0.2,
                "top_p": 0.9,
                "return_citations": True,
                "search_domain_filter": ["perplexity.ai"],
                "return_images": False,
                "return_related_questions": False,
                "search_recency_filter": "month",
                "top_k": 0,
                "stream": False,
                "presence_penalty": 0,
                "frequency_penalty": 1
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract answer
                answer = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                
                # Extract sources/citations
                sources = []
                citations = data.get("citations", [])
                for citation in citations:
                    if isinstance(citation, str):
                        sources.append(citation)
                    elif isinstance(citation, dict) and "url" in citation:
                        sources.append(citation["url"])
                
                # Remove duplicates while preserving order
                unique_sources = []
                for source in sources:
                    if source not in unique_sources:
                        unique_sources.append(source)
                
                result = PerplexityResult(
                    question=question,
                    answer=answer,
                    sources=unique_sources,
                    timestamp=datetime.now()
                )
                
                self.logger.info(f"Successfully got Perplexity answer for: {question[:50]}...")
                return result
                
            else:
                self.logger.error(f"Perplexity API error {response.status_code}: {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Network error calling Perplexity API: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error calling Perplexity API: {e}")
            return None
    
    def validate_api_key(self) -> bool:
        """
        Validate the API key by making a test request.
        
        Returns:
            True if API key is valid, False otherwise
        """
        try:
            test_result = self.ask_question("What is AI?")
            return test_result is not None
        except Exception as e:
            self.logger.error(f"API key validation failed: {e}")
            return False
    
    def get_available_models(self) -> List[str]:
        """
        Get list of available models.
        
        Returns:
            List of model names
        """
        try:
            response = requests.get(
                f"{self.base_url}/models",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                models = [model.get("id", "") for model in data.get("data", [])]
                return [model for model in models if model]
            else:
                self.logger.error(f"Failed to get models: {response.status_code}")
                return []
                
        except Exception as e:
            self.logger.error(f"Error getting available models: {e}")
            return []
    
    def get_usage_info(self) -> Optional[Dict[str, Any]]:
        """
        Get API usage information if available.
        
        Returns:
            Dictionary with usage info or None
        """
        try:
            # Note: This endpoint may not exist in Perplexity API
            # This is a placeholder for potential future functionality
            response = requests.get(
                f"{self.base_url}/usage",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
                
        except Exception as e:
            self.logger.debug(f"Usage info not available: {e}")
            return None