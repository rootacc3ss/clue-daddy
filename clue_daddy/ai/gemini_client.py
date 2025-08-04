"""
Gemini API client for AI assistant functionality.
"""

import google.generativeai as genai
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime


class GeminiClient:
    """Client for interacting with Google Gemini API."""
    
    def __init__(self, api_key: str, model_name: str = "gemini-live-2.5-flash-preview"):
        self.api_key = api_key
        self.model_name = model_name
        self.logger = logging.getLogger(__name__)
        
        # Configure the API
        genai.configure(api_key=api_key)
        
        # Initialize the model
        try:
            self.model = genai.GenerativeModel(model_name)
            self.logger.info(f"Initialized Gemini model: {model_name}")
        except Exception as e:
            self.logger.error(f"Failed to initialize Gemini model: {e}")
            self.model = None
    
    def validate_api_key(self) -> bool:
        """
        Validate the API key by making a test request.
        
        Returns:
            True if API key is valid, False otherwise
        """
        try:
            if not self.model:
                return False
                
            # Make a simple test request
            response = self.model.generate_content("Hello")
            return response and hasattr(response, 'text')
            
        except Exception as e:
            self.logger.error(f"API key validation failed: {e}")
            return False
    
    def generate_response(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> Optional[str]:
        """
        Generate a response from Gemini.
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt for context
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens in response
            
        Returns:
            Generated response text or None if failed
        """
        try:
            if not self.model:
                self.logger.error("Gemini model not initialized")
                return None
            
            # Combine system prompt and user prompt if system prompt provided
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\nUser: {prompt}"
            
            # Configure generation parameters
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            )
            
            # Generate response
            response = self.model.generate_content(
                full_prompt,
                generation_config=generation_config
            )
            
            if response and hasattr(response, 'text'):
                self.logger.debug(f"Generated response for prompt: {prompt[:50]}...")
                return response.text
            else:
                self.logger.error("No text in Gemini response")
                return None
                
        except Exception as e:
            self.logger.error(f"Error generating Gemini response: {e}")
            return None
    
    def generate_response_with_image(
        self,
        prompt: str,
        image_data: bytes,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> Optional[str]:
        """
        Generate a response from Gemini with image analysis.
        
        Args:
            prompt: The user prompt
            image_data: Screenshot or image data as bytes
            system_prompt: Optional system prompt for context
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
            
        Returns:
            Generated response text or None if failed
        """
        try:
            if not self.model:
                self.logger.error("Gemini model not initialized")
                return None
            
            # Prepare the image
            import PIL.Image
            import io
            
            image = PIL.Image.open(io.BytesIO(image_data))
            
            # Combine system prompt and user prompt if system prompt provided
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\nUser: {prompt}"
            
            # Configure generation parameters
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            )
            
            # Generate response with image
            response = self.model.generate_content(
                [full_prompt, image],
                generation_config=generation_config
            )
            
            if response and hasattr(response, 'text'):
                self.logger.debug(f"Generated image response for prompt: {prompt[:50]}...")
                return response.text
            else:
                self.logger.error("No text in Gemini image response")
                return None
                
        except Exception as e:
            self.logger.error(f"Error generating Gemini image response: {e}")
            return None
    
    def start_chat_session(self, system_prompt: Optional[str] = None) -> Optional['GeminiChatSession']:
        """
        Start a chat session for continuous conversation.
        
        Args:
            system_prompt: Optional system prompt for the session
            
        Returns:
            GeminiChatSession object or None if failed
        """
        try:
            if not self.model:
                self.logger.error("Gemini model not initialized")
                return None
            
            # Start chat session
            chat = self.model.start_chat(history=[])
            
            # Send system prompt if provided
            if system_prompt:
                chat.send_message(system_prompt)
            
            return GeminiChatSession(chat, self.logger)
            
        except Exception as e:
            self.logger.error(f"Error starting chat session: {e}")
            return None
    
    def get_available_models(self) -> List[str]:
        """
        Get list of available Gemini models.
        
        Returns:
            List of model names
        """
        try:
            models = genai.list_models()
            model_names = [model.name for model in models if 'generateContent' in model.supported_generation_methods]
            return model_names
        except Exception as e:
            self.logger.error(f"Error getting available models: {e}")
            return []


class GeminiChatSession:
    """Wrapper for Gemini chat session."""
    
    def __init__(self, chat_session, logger):
        self.chat = chat_session
        self.logger = logger
        self.history = []
    
    def send_message(self, message: str) -> Optional[str]:
        """
        Send a message in the chat session.
        
        Args:
            message: Message to send
            
        Returns:
            Response text or None if failed
        """
        try:
            response = self.chat.send_message(message)
            
            if response and hasattr(response, 'text'):
                # Store in history
                self.history.append({
                    'user': message,
                    'assistant': response.text,
                    'timestamp': datetime.now()
                })
                
                return response.text
            else:
                self.logger.error("No text in chat response")
                return None
                
        except Exception as e:
            self.logger.error(f"Error sending chat message: {e}")
            return None
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get chat history."""
        return self.history.copy()
    
    def clear_history(self):
        """Clear chat history."""
        self.history.clear()