import os
import sys
import atexit
from dotenv import load_dotenv
from bin.helper.banner import banner
from bin.chat import auth, chat

try:
    import readline
except ImportError:
    readline = None

def save_history(histfile):
    try:
        readline.write_history_file(histfile)
    except Exception:
        pass

def setup_readline():
    if not readline:
        return
    histfile = os.path.expanduser("~/.edith_history")
    try:
        if not os.path.exists(os.path.dirname(histfile)):
            os.makedirs(os.path.dirname(histfile), exist_ok=True)
        readline.read_history_file(histfile)
        readline.set_history_length(1000)
    except FileNotFoundError:
        pass
    except Exception:
        pass
    atexit.register(save_history, histfile)

def load_environment():
    load_dotenv(os.path.expanduser("~/.env"))
    api_key = os.environ.get('EDITH_API') or os.environ.get('OPENAI_API_KEY')
    base_url = os.environ.get('EDITH_URL')
    model = os.environ.get('EDITH_MODEL')
    
    if not api_key or not model:
        sys.stdout.write("\033[31m[Error]\033[0m Missing EDITH_API or EDITH_MODEL in ~/.env\n")
        sys.exit(1)
        
    return api_key, base_url, model

def handle_command(query, history):
    cmd = query.lower()
    if cmd in {'/exit', 'exit', 'quit'}:
        return False, history
    if cmd in {'/clear', 'clear'}:
        sys.stdout.write("\033c")
        sys.stdout.flush()
        banner()
        sys.stdout.write("\033[90mSession memory cleared.\033[0m\n\n")
        return True, []
    if cmd in {'/help', 'help'}:
        sys.stdout.write("\n\033[1mCOMMANDS:\033[0m\n  /clear - Reset memory\n  /exit  - Quit application\n  /help  - Show this menu\n\n")
        return True, history
    return None, history

def main():
    setup_readline()
    api_key, base_url, model = load_environment()
    
    try:
        client = auth(api_key, base_url)
    except Exception as e:
        sys.stdout.write(f"\033[31m[Auth Error]\033[0m {e}\n")
        sys.exit(1)
    
    prompt = "\001\033[90m\002>\001\033[0m\002 "
    history = []
    
    sys.stdout.write("\033c")
    sys.stdout.flush()
    banner()
    
    while True:
        try:
            query = input(prompt).strip()
            if not query:
                continue
                
            status, history = handle_command(query, history)
            if status is False:
                sys.stdout.write("\n")
                break
            if status is True:
                continue
                
            new_interactions = chat(client, query, history, model)
            if new_interactions:
                history.extend(new_interactions)
            
        except EOFError:
            sys.stdout.write("\n")
            break
        except KeyboardInterrupt:
            sys.stdout.write("\n")
            sys.stdout.flush()
            continue
        except Exception as e:
            sys.stdout.write(f"\n\033[31m[Error]\033[0m {e}\n\n")
            sys.stdout.flush()
    sys.exit(0)

if __name__ == "__main__":
    main()
