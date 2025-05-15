import os
from typing import List, Dict
import requests
import json

class ChatManager:
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.chat_history = []

    def add_message(self, role: str, content: str) -> None:
        """Add a message to the chat history."""
        self.chat_history.append({"role": role, "content": content})

    def get_chat_history(self) -> List[Dict[str, str]]:
        """Get the chat history."""
        return self.chat_history

    def get_response(self, query: str, relevant_chunks: List[str]) -> str:
        """Generate a response using the OpenRouter API."""
        # Combine relevant chunks into context
        context = "\n".join(relevant_chunks)

        # Create the system message with instructions
        system_message = {
            "role": "system",
            "content": """You are a helpful AI assistant that answers questions based on the provided document context. 
            Your responses should be:
            1. Accurate and based only on the provided context
            2. Clear and well-structured
            3. Natural and conversational
            4. Complete - do not cut off mid-sentence
            If you cannot find the answer in the context, say so honestly."""
        }

        # Create the user message with context and query
        user_message = {
            "role": "user",
            "content": f"""Context: {context}\n\nQuestion: {query}"""
        }

        # Prepare the request
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "Document Chat"
        }

        # Combine all messages
        messages = [system_message] + self.chat_history + [user_message]

        data = {
            "model": "mistralai/mistral-7b-instruct",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1000,  # Increased token limit for complete answers
            "stream": False
        }

        try:
            # Make the API request
            response = requests.post(self.api_url, headers=headers, json=data)
            
            # Print response details for debugging
            print(f"Response Status: {response.status_code}")
            print(f"Response Headers: {response.headers}")
            print(f"Response Content: {response.text}")
            
            response.raise_for_status()  # Raise an exception for bad status codes
            
            # Parse the response
            response_data = response.json()
            response_text = response_data["choices"][0]["message"]["content"]

            # Add the response to chat history
            self.add_message("assistant", response_text)

            return response_text

        except requests.exceptions.RequestException as e:
            error_message = f"API Error: {str(e)}"
            if hasattr(e.response, 'text'):
                error_message += f"\nResponse: {e.response.text}"
            self.add_message("assistant", error_message)
            return error_message
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            self.add_message("assistant", error_message)
            return error_message 