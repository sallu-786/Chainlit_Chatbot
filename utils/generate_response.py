import os
from litellm import acompletion
import chainlit as cl
from utils.prompts import DEFAULT_PROMPT,DATA_ANALYST_PROMPT,VISUAL_ANALYST_PROMPT,DOCUMENT_ANALYST_PROMPT,CODE_ANALYST_PROMPT
from dotenv import load_dotenv
load_dotenv()

os.getenv("AZURE_API_KEY")
os.getenv("AZURE_API_BASE")
os.getenv("AZURE_API_VERSION")


class GenerateResponse:
    def __init__(self):
        
        self.MODELS = {
        "ChatGPT-4": "azure/azure_openai_app_4o",
        "phi": "ollama/phi4:latest",
        "vision": "ollama/llava:13b",
        "code": "ollama/qwen2.5-coder:14b",
        "reason": "ollama/deepseek-r1:14b",
        }       
        self.model = self.MODELS['ChatGPT-4']                                                             #Default model
        # self.api_base = os.getenv("LITELLM_API_BASE", "http://localhost:11434")                         #Default API base
        self.system_msg = DEFAULT_PROMPT                                                                
        self.system_msg_tabular = DATA_ANALYST_PROMPT
        self.system_msg_code = CODE_ANALYST_PROMPT
        self.system_msg_image = VISUAL_ANALYST_PROMPT
        self.system_msg_document = DOCUMENT_ANALYST_PROMPT

        
    async def generate_streaming_response(self, model_select, user_message, input_documents: list = [], chat_history: list = []):
        messages = []
        is_dynamic = (model_select == "dynamic")
         
        for chat in chat_history[-2:]:
            if isinstance(chat, dict) and "role" in chat and "content" in chat:
                messages.append(chat)

        if input_documents:

            for doc in input_documents:
                if doc['category'] == 'image':
                    self.model = self.MODELS["vision"] if is_dynamic else model_select
                    messages.extend([
                        {"role": "system", "content": self.system_msg_image},
                        {"role": "user", "content": [{"type": "text", "text": f"User Message: \t{user_message} \n"}]},
                        {"role": "user", "content": doc['data']}
                    ])
                    
                elif doc['category'] == "code":
                    self.model = self.MODELS["code"] if is_dynamic else model_select
                    messages.extend([
                        {"role": "system", "content": self.system_msg_code},
                        {"role": "user", "content": [{"type": "text", "text": f"User Message: \t{user_message} \n"}]},
                        {"role": "user", "content": [{"type": "text", "text": f"File_Name: \t {doc['file_name']} \n Code_Content:\t {doc['data']}"}]}
                    ])
                    
                elif doc['category'] == "document":
                    self.model = self.MODELS["reason"] if is_dynamic else model_select
                    messages.extend([
                        {"role": "system", "content": self.system_msg_document},
                        {"role": "user", "content": [{"type": "text", "text": f"User Message: \t{user_message} \n"}]},
                        {"role": "user", "content": [{"type": "text", "text": f"File_Name: \t {doc['file_name']} \n File_Content:\t {doc['data']}"}]}
                    ])

                elif doc['category'] == "tabular":
                    self.model = self.MODELS["reason"] if is_dynamic else model_select
                    messages.extend([
                        {"role": "system", "content": self.system_msg_document},
                        {"role": "user", "content": [{"type": "text", "text": f"User Message: \t{user_message} \n"}]},
                        {"role": "user", "content": [{"type": "text", "text": f"File_Name: \t {doc['file_name']} \n File_Content:\t {doc['data']}"}]}
                    ])

            # await cl.Message(content=f"Responding Model:{self.model}").send()
        else:
            self.model = self.MODELS["phi"] if is_dynamic else model_select 
            # await cl.Message(content=f"Responding Model:{self.model}").send()
            messages.extend([
                {"role": "system", "content": self.system_msg},
                {"role": "user", "content": [{"type": "text", "text": f"User Message: \t{user_message} \n"}]}
            ])
        try:
            response = await acompletion(
                model=self.model,
                messages=messages,
                stream=True 
            )                    
            async for chunk in response:
                yield chunk  
        except Exception as e:
            await cl.Message(content=f"🚨 Failed to get response: {e} 🚨").send()
            raise RuntimeError(f"Failed to get response: {e}")
