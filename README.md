# Code-Edith (code-edith)

## 1. What It Is
Code-Edith is a privacy focused Python Local/Cloud AI Agent.

After installation, run it directly:

    code-edith

Supports tool calling:
- web_search
- read_file
- list_dir
- get_os_info
- date_time


## 2. Requirements
- Python 3.10+
- OpenAI-compatible API (cloud or local)


## 3. Installation

Install using pip:

    pip install code-edith

After installation, start it with:

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
    EDITH_URL

Using Local Models (OpenAI-Compatible Servers):

Works with local servers like llama.cpp or any OpenAI-compatible endpoint.

For local usage:
- Only EDITH_URL is strictly required.
- EDITH_API can be dummy or ignored (if server allows).
- EDITH_MODEL depends on server requirements/any

Example local config:

    EDITH_URL=http://localhost:8000/v1
    EDITH_MODEL=your-local-model-name
    EDITH_API=dummy

Note:
- Local models must support tool calling.
- Models without tool calling support will not work correctly and will crash


## 5. CLI Commands

Inside app:

    /help
    /clear
    /exit

Session memory:
- Stored only during runtime
- Cleared with /clear
- History saved in ~/.edith_history (only prompts sent by user)

## 7. Uninstall

    pip uninstall code-edith
