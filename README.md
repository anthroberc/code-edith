# Code-Edith (code-edith)

## 1. What It Is
Code-Edith is a Python CLI AI assistant.  
Run after install:

    code-edith

Supports tool calling:
- web_search
- read_file
- list_dir
- get_os_info
- date_time


## 2. Requirements
- Python 3.10+
- pip
- OpenAI-compatible API (cloud or local)


## 3. Installation
    
    cd Edith-Code
    pip install .

Run:

    code-edith


## 4. Environment Setup (~/.env)

Location:
- Linux / Termux: ~/.env
- Windows: C:\Users\YourName\.env

Example:

    EDITH_API=your_api_key
    EDITH_MODEL=gpt-4o-mini
    EDITH_URL=https://api.openai.com/v1


Important:

- Every environment variable is important for normal cloud usage.
- Minimum for cloud APIs:
    EDITH_API
    EDITH_MODEL

Using Local Models (OpenAI-Compatible Servers):

Works with local servers like llama.cpp or any OpenAI-compatible endpoint.

For local usage:
- Only EDITH_URL is strictly required.
- EDITH_API can be dummy or ignored (if server allows).
- EDITH_MODEL depends on server requirements.

Example local config:

    EDITH_URL=http://localhost:8000/v1
    EDITH_MODEL=your-local-model-name
    EDITH_API=dummy

Note:
- Local models must support tool calling.
- Models without tool calling support will not work correctly.


## 5. CLI Commands

Inside app:

    /help
    /clear
    /exit

Session memory:
- Stored only during runtime
- Cleared with /clear
- History saved in ~/.edith_history


## 6. Limitations

- Requires API endpoint (cloud or local)
- Terminal only (no GUI)
- No persistent memory
- Tool access depends on OS permissions
- Local models must support tool calling


## 7. Uninstall

    pip uninstall code-edith


All Rights Reserved
