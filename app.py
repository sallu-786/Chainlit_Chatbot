import chainlit as cl
from chainlit.input_widget import Switch,Select
from utils.generate_response import GenerateResponse
from utils.file_handler import FileHandler
system = GenerateResponse()
models=system.MODELS
IS_PERSIST=False

@cl.on_chat_start
async def on_chat_start():
   
    cl.user_session.set("processed_files", None)
    cl.user_session.set("chat_history", [])
    settings = await cl.ChatSettings(
        [
            Switch(id="persist", label="Persist File Upload", initial=IS_PERSIST),
            Select(
                id="model-selection",
                label="Model Selection-Mode",
                values = ["dynamic"] + [v for _, v in models.items()],
                initial_index=1,                                                             # 0 index for dynamic model selection
            ),
        ]
    ).send()
    cl.user_session.set("settings", settings)
    
@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="High perormance tasks in C++",
            message="Explore solutions in C++ for efficient and high-performance programming tasks",
            icon="/public/c.png",
            ),

        cl.Starter(
            label="Visual Basic For Loop",
            message="How to write a for loop in VBA that activates after pushing the button",
            icon="/public/vba.png",
            ),
        cl.Starter(
            label="Python script for email reports",
            message="Write a script to automate sending daily email reports in Python, and walk me through how I would set it up.",
            icon="/public/python.png",
            ),
        cl.Starter(
            label="Microsoft Power App Development",
            message="How to create an attendence Management system in Microsoft Power Platofrm. Give me a step by step guide in Japanese?",
            icon="/public/pa.png",
            )
        ]

@cl.on_message
async def on_message(input_message: cl.Message):

    settings = cl.user_session.get("settings")                                                               
    model_select = settings.get("model-selection")
    
    persist = settings.get("persist")      
    if persist:
        processed_files = cl.user_session.get("processed_files")
    else: 
        processed_files = None

    user_message = input_message.content
    chat_history = cl.user_session.get("chat_history", [])
    chat_history.append({"role": "user", "message": user_message})
 

    if input_message.elements:
        processed_files = []                                                                            # List to store processed content for all files
        python_files = [file for file in input_message.elements]                                        # Collect all files

        for python_file in python_files:                                                                # Loop through file list
        
            handler = FileHandler(python_file)  
            python_content = handler.process_file()                                                        # Initialize handler for each file
            
            if python_content is None:
                await cl.Message(content=f"🚨 File format unsupported!!... LLM will continue without input documents 🚨").send()

            else:
                if python_content['category']=='image':
                    processed_files.append({

                    "category":f"{python_content['category']}",
                    "data": [
                        {   
                            "type": "text",
                            "text": f"File_Name: \t {python_content['file_name']}" 
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url":f"{python_content['data']}"}
                        }
                    ]
                    })
                else:
                    processed_files.append(python_content)

        
        cl.user_session.set("processed_files", processed_files)                                     # Store processed files in session


    try:
        if processed_files:                                                                         #Check if user uploaded file

            stream = system.generate_streaming_response(model_select, user_message, processed_files, chat_history)
        else:

            stream = system.generate_streaming_response(model_select, user_message,[],chat_history) # [] bcos no input document


    except Exception as e:
        print(f"Failed to get Response from LLM: {e}")
        
        return
    
    reply = cl.Message(content="")
    async for chunk in stream:
        if token := chunk.choices[0].delta.content:
            await reply.stream_token(token)
    chat_history.append({"role": "assistant", "content": reply.content})
    cl.user_session.set("chat_history", chat_history)
    await reply.update()