import chainlit as cl
from response2 import GenerateResponse
from file_handler2 import FileHandler

system = GenerateResponse()

@cl.on_chat_start
async def on_chat_start():
    # Initialize empty session storage for file
    cl.user_session.set("processed_files", None)

@cl.on_message
async def on_message(input_message: cl.Message):
    user_message = input_message.content
    processed_files = cl.user_session.get("processed_files")
 

    if input_message.elements:
        processed_files = []  # List to store processed content for all files
        python_files = [file for file in input_message.elements]  # Collect all files

        for python_file in python_files:  # Loop through each file

            handler = FileHandler(python_file)  # Initialize handler for each file
            python_content = handler.process_file()

            if python_content is not None:
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

        cl.user_session.set("processed_files", processed_files)  # Store processed files in session

    # Construct the input for GenerateResponse
    try:
        if processed_files:
            # rag_query = f"Context: {processed_files}\nQuestion: {user_message}"
            stream = system.generate_streaming_response(user_message,processed_files)
        else:
            # Handle the case where no files are uploaded
            stream = system.generate_streaming_response(user_message,[])

    except Exception as e:
        print(f"Failed to get Response from ChatGPT: {e}")
        return
    print(stream)
    # Stream the response back to the user
    reply = cl.Message(content="")
    async for chunk in stream:
        if token := chunk.choices[0].delta.content:
            await reply.stream_token(token)
    await reply.update()