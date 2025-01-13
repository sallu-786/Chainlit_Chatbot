import os
from dotenv import load_dotenv
from litellm import acompletion


load_dotenv()
MODEL= "ollama/llama3.1"

class GenerateResponse:
    def __init__(self):
        self.system_msg_code = """You are an expert coding assistant specializing in software development. Please follow these guidelines:

        Core Behaviors:
        - Explain code simply, assuming the user is a beginner.
        - Keep responses concise and focused on the specific question."""
        
        self.system_msg_image = """You are helpful assistant, an expert in analyzing images. Please follow these guidelines:

        Core Behaviors:
        - Explain contet of the image.
        - Fulfill the taks user asks to do while using the image(s)."""

        self.system_msg_document = """You are helpful assistant, an expert in analyzing document. Please follow these guidelines:

        Core Behaviors:
        - Answer the questions of user based on the document.
        - If the rlevant content is not in documents say you dont know."""

        self.system_msg = """You are helpful assistant. answer questions of user"""

        self.api_base = os.getenv("LITELLM_API_BASE", "http://localhost:11434")  # Default API base
        self.model = MODEL  # Default model for litellm

    async def generate_streaming_response(self, user_message, input_documents: list = []):
        messages = []

        if input_documents:
            for doc in input_documents:
                if doc['category'] == 'image':
                    messages.append({"role": "system", "content": self.system_msg_image})
                    messages.append({
                        "role": "user", 
                        "content": [{"type": "text", "text": f"User Message: \t{user_message} \n"}]
                    })
                    messages.append({"role": "user", "content": doc['data']})
                    
                elif doc['category'] == "code":
                    messages.append({"role": "system", "content": self.system_msg_code})
                    messages.append({
                        "role": "user", 
                        "content": [{"type": "text", "text": f"User Message: \t{user_message} \n"}]
                    })
                    messages.append({
                        "role": "user", 
                        "content": [{"type": "text", "text": f"File_Name: \t {doc['file_name']} \n Code_Content:\t {doc['data']}"}]
                    })
                    
                elif doc['category'] == "document" or doc['category'] == "pandas":
                    messages.append({"role": "system", "content": self.system_msg_document})
                    messages.append({
                        "role": "user", 
                        "content": [{"type": "text", "text": f"User Message: \t{user_message} \n"}]
                    })
                    messages.append({
                        "role": "user", 
                        "content": [{"type": "text", "text": f"File_Name: \t {doc['file_name']} \n File_Content:\t {doc['data']}"}]
                    })
        else:
            messages.append({"role": "system", "content": self.system_msg})
            messages.append({
                "role": "user", 
                "content": [{"type": "text", "text": f"User Message: \t{user_message} \n"}]
            })
        try:
            response = await acompletion(
                model=self.model,
                messages=messages,
                stream=True 
            )                    
            async for chunk in response:
                yield chunk  
        except Exception as e:
            raise RuntimeError(f"Failed to get response: {e}")
