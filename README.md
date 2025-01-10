# Chainlit_Chatbot
This is a Web Application made using chainlit. It includes an intelligent file analysis system built with Chainlit that processes various file types and generates contextual responses using LLM. The system supports multiple file formats including images, code files, documents, and spreadsheets.

## System Architecture
![image](https://github.com/user-attachments/assets/c94bb7a9-2ddb-4a82-b82d-38fff73a9740)


## Features

- **Multi-format File Processing**: Supports various file formats including:
  - Images (JPEG, PNG)
  - Code files (Python, JSON)
  - Documents (PDF, DOCX, PPTX, TXT)
  - Spreadsheets (CSV, XLSX)
- **Streaming Responses**: Real-time response generation using LiteLLM
- **Context-Aware Analysis**: Different processing strategies for different file types
- **Interactive UI**: Built with Chainlit for seamless user interaction

- **Dynamic Coontext-Aware Prompting**: Automatically gives best prompt/instructions to LLM based on type of file attached while keeping the token count short
  When a file is uploaded, the system follows these steps:

  - The FileHandler determines the category of the file (Image/Code/Text document/spreadsheets/None)
  - This category information is stored in the processed file's metadata
  - When the GenerateResponse class receives this information, it activates the appropriate expert prompt
  - If no file attached(None category) default prompt is used

![image](https://github.com/user-attachments/assets/d9ac8f69-66c9-4615-9255-10ae203ff1aa)


## Prerequisites

- Python 3.11+
- LLM API/ Ollama (for Open source)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-file-analysis.git
cd ai-file-analysis
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```


2. Ensure all required dependencies are installed (see requirements.txt below)

## Usage

1. Start the Chainlit server:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 
```

2. Open your browser and navigate to `http://localhost:8000/codepilot`

3. Upload files and interact with the assistant through the UI

## Project Structure

```
.
├── app.py                 # Main application file with Chainlit setup
├── file_handler.py       # File processing and categorization logic
├── response.py           # LLM response generation handling
├── requirements.txt       # Project dependencies
```

## Contact
For query/projects/consultancy please contact me at suleman.muhammad08@gmail.com

## License

This project is licensed under the MIT License - Please give it a star if it helps
