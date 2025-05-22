import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage

import re
class TextSummarizer:
    """
    AI-powered text summarization using Google Gemini 1.5 Flash via LangChain
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the summarizer with Google API key
        
        Args:
            api_key (str): Google API key for Gemini access
        """
        self.api_key = api_key
        self.model = self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the Gemini model through LangChain"""
        try:
            model = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=self.api_key,
                temperature=0.3,
                max_tokens=1024,
                timeout=30,
                max_retries=2
            )
            return model
        except Exception as e:
            raise Exception(f"Failed to initialize Gemini model: {str(e)}")
    
    def _preprocess_text(self, text: str) -> str:
        """
        Clean and preprocess the input text
        
        Args:
            text (str): Raw input text
            
        Returns:
            str: Cleaned text
        """
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters that might cause issues
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)\[\]\{\}\"\'\/]', '', text)
        
        # Trim whitespace
        text = text.strip()
        
        return text
    
    def _create_prompt(self, text: str, style: str, max_words: int, language: str) -> str:
        """
        Create a structured prompt for the AI model
        
        Args:
            text (str): Text to summarize
            style (str): Summary style (brief, detailed, bullet points)
            max_words (int): Maximum words in summary
            language (str): Output language
            
        Returns:
            str: Formatted prompt
        """
        style_instructions = {
            "brief": "Create a concise, brief summary that captures only the most essential points.",
            "detailed": "Create a comprehensive summary that covers all important points and key details.",
            "bullet points": "Create a summary in bullet point format, highlighting key points clearly."
        }
        
        style_instruction = style_instructions.get(style, style_instructions["brief"])
        
        prompt = f"""
You are an expert text summarizer. Your task is to create a high-quality summary of the provided text.

INSTRUCTIONS:
- {style_instruction}
- Maximum length: approximately {max_words} words
- Output language: {language}
- Maintain the original meaning and context
- Use clear, professional language
- Focus on key facts, main ideas, and important details
- Do not add information not present in the original text

TEXT TO SUMMARIZE:
{text}

SUMMARY:
"""
        
        return prompt
    
    def summarize_text(self, text: str, style: str = "brief", max_words: int = 150, language: str = "english") -> str:
        """
        Generate a summary of the provided text
        
        Args:
            text (str): Text to summarize
            style (str): Summary style - "brief", "detailed", or "bullet points"
            max_words (int): Maximum words in the summary
            language (str): Output language
            
        Returns:
            str: Generated summary
            
        Raises:
            Exception: If summarization fails
        """
        try:
            # Preprocess the input text
            cleaned_text = self._preprocess_text(text)
            
            if len(cleaned_text.split()) < 10:
                raise Exception("Text is too short for meaningful summarization (minimum 10 words required)")
            
            # Create the prompt
            prompt = self._create_prompt(cleaned_text, style, max_words, language)
            
            # Create system and human messages
            system_message = SystemMessage(
                content="You are a professional text summarizer. Provide accurate, concise, and well-structured summaries."
            )
            human_message = HumanMessage(content=prompt)
            
            # Generate summary
            messages = [system_message, human_message]
            response = self.model(messages)
            
            # Extract and clean the summary
            summary = response.content.strip()
            
            # Remove any unwanted prefixes that the model might add
            unwanted_prefixes = ["SUMMARY:", "Summary:", "Here is the summary:", "Here's the summary:"]
            for prefix in unwanted_prefixes:
                if summary.startswith(prefix):
                    summary = summary[len(prefix):].strip()
            
            if not summary:
                raise Exception("Generated summary is empty")
            
            return summary
            
        except Exception as e:
            # Provide more specific error messages
            if "quota" in str(e).lower():
                raise Exception("API quota exceeded. Please check your Google Cloud billing and quota limits.")
            elif "authentication" in str(e).lower() or "api key" in str(e).lower():
                raise Exception("Authentication failed. Please verify your Google API key is correct and has proper permissions.")
            elif "timeout" in str(e).lower():
                raise Exception("Request timed out. Please try again with shorter text or check your internet connection.")
            else:
                raise Exception(f"Summarization failed: {str(e)}")
    
    def validate_api_key(self) -> bool:
        """
        Validate if the API key is working
        
        Returns:
            bool: True if API key is valid, False otherwise
        """
        try:
            # Test with a simple prompt
            test_message = HumanMessage(content="Hello, please respond with 'API key is working'")
            response = self.model([test_message])
            return bool(response.content)
        except:
            return False
    
    def get_model_info(self) -> dict:
        """
        Get information about the current model
        
        Returns:
            dict: Model information
        """
        return {
            "model_name": "gemini-1.5-flash",
            "provider": "Google",
            "framework": "LangChain",
            "max_tokens": 1024,
            "temperature": 0.3
        }
