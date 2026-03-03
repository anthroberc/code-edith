# Code-Edith (code-edith)

Beginner Friendly Guide

---------------------------------------
1. What is Code-Edith?
---------------------------------------

Code-Edith is a CLI (Command Line Interface) AI assistant written in Python.

After installation, you start it using:

    code-edith

It runs in your terminal and allows you to chat with an AI model.
It supports tools like:
- Web search (DuckDuckGo via ddgs)
- Read file
- List directory
- OS information
- Date and time

---------------------------------------
2. Requirements
---------------------------------------

Before installing, make sure you have:

- Python 3.10 or newer
- pip (Python package manager)
- Internet connection
- An OpenAI-compatible API key

Dependencies used internally:
- openai==2.24.0
- python-dotenv
- rich
- ddgs

---------------------------------------
3. Installation
---------------------------------------

If you have the project folder:

Step 1: Go inside the project folder

    cd Edith-Code

Step 2: Install the package

    pip install .

After successful installation, you can run:

    code-edith

---------------------------------------
4. Environment Setup (.env file)
---------------------------------------

Code-Edith requires a .env file in your HOME directory.

Location of .env:

Linux / Termux:
    ~/.env

Windows:
    C:\Users\YourName\.env

Create the file:

    touch ~/.env

Inside ~/.env, add:

    EDITH_API=your_api_key_here
    EDITH_MODEL=gpt-4o-mini
    EDITH_URL=https://api.openai.com/v1

Minimum required:

    EDITH_API
    EDITH_MODEL

Alternative:
You can use OPENAI_API_KEY instead of EDITH_API.

Example minimal config:

    EDITH_API=sk-xxxxxxxxxxxxxxxx
    EDITH_MODEL=gpt-4o-mini

If EDITH_API or EDITH_MODEL is missing, the app will stop with:

    [Error] Missing EDITH_API or EDITH_MODEL in ~/.env

---------------------------------------
5. Running Code-Edith
---------------------------------------

Start the application:

    code-edith

You will see a banner.
Then you can start typing prompts.

Example:

    > explain python decorators
    > list files in current directory
    > search latest AI news

---------------------------------------
6. Built-in Commands
---------------------------------------

Inside the CLI:

/help      Show help menu  
/clear     Clear session memory  
/exit      Exit the application  

You can also type:

    exit
    quit
    clear
    help

---------------------------------------
7. How Session Memory Works
---------------------------------------

- The app stores conversation history in memory during the session.
- When you use /clear, it resets memory.
- When you exit, memory is lost.
- Command history is saved in:

    ~/.edith_history

---------------------------------------
8. Tools Available
---------------------------------------

The system includes tool support such as:

- web_search
- read_file
- list_dir
- get_os_info
- data_time

The AI decides when to call these tools automatically.

---------------------------------------
9. Limitations
---------------------------------------

1. Requires Internet  
   It depends on external API and web search.

2. No Offline Mode  
   It cannot run local models without modifying the code.

3. No GUI  
   Terminal only.

4. No Persistent Memory  
   Memory resets after exit.

5. Depends on API Stability  
   If your API key is invalid or rate-limited, it will fail.

6. Tool Security  
   File reading and directory listing depend on OS permissions.

---------------------------------------
10. Common Errors
---------------------------------------

[Auth Error]
- Invalid API key
- Wrong EDITH_URL

Missing EDITH_API or EDITH_MODEL
- Your ~/.env file is not configured correctly

---------------------------------------
11. Uninstall
---------------------------------------

To remove:

    pip uninstall code-edith

---------------------------------------
12. Developer Notes
---------------------------------------

Entry point:

    code-edith = index:main

Main file:

    index.py

---------------------------------------

All Rights Reserved
