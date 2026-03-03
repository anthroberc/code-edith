import os, json, glob, importlib.util, sys, time
from concurrent.futures import ThreadPoolExecutor
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live
from rich.text import Text
from rich.table import Table

console = Console(width=min(max(Console().width, 40), 100))
CACHE = {"tools": {}, "sys": None, "conf": None}

def auth(k, u): 
    return OpenAI(api_key=k, base_url=u)

def get_sys():
    if not CACHE["sys"]:
        try:
            with open(os.path.join(os.path.dirname(__file__), "system.txt"), "r") as f:
                CACHE["sys"] = f.read().strip()
        except: 
            CACHE["sys"] = "You are a helpful assistant."
    return CACHE["sys"]

def get_conf():
    if CACHE["conf"] is None:
        p = os.path.join(os.path.dirname(__file__), "tools.json")
        if os.path.exists(p):
            with open(p, "r") as f: 
                CACHE["conf"] = json.load(f)
    return CACHE["conf"]

def get_func(n):
    if n in CACHE["tools"]: return CACHE["tools"][n]
    for p in glob.glob(os.path.join(os.path.dirname(__file__), "tool", "*.py")):
        try:
            spec = importlib.util.spec_from_file_location(os.path.basename(p)[:-3], p)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            if hasattr(mod, n):
                CACHE["tools"][n] = getattr(mod, n)
                return CACHE["tools"][n]
        except: 
            continue
    return None

def run_tool(n, mid, a_str):
    try: 
        args = json.loads(a_str or "{}")
    except: 
        return {"role": "tool", "tool_call_id": mid, "name": n, "content": "Error: Invalid JSON"}
    f = get_func(n)
    if not f: 
        return {"role": "tool", "tool_call_id": mid, "name": n, "content": "Error: Not found"}
    try: 
        return {"role": "tool", "tool_call_id": mid, "name": n, "content": str(f(**args))}
    except Exception as e: 
        return {"role": "tool", "tool_call_id": mid, "name": n, "content": str(e)}

def _clear_animation(active):
    if active:
        sys.stdout.write("\r" + " "*50 + "\r")
        sys.stdout.flush()
    return False

def _update_animation(active, dots, last_anim):
    curr_time = time.time()
    if curr_time - last_anim > 0.3:
        dots = (dots + 1) % 4
        sys.stdout.write(f"\r\033[38;2;217;119;87m>\033[0m \033[90mReasoning{'.' * dots:<3}\033[0m")
        sys.stdout.flush()
        return True, dots, curr_time
    return active, dots, last_anim

def _md(text):
    grid = Table.grid()
    grid.add_column(width=2)
    grid.add_column()
    grid.add_row(Text("> ", style="#d97757"), Markdown(text))
    return grid

def build_kwargs(model, msgs, tools=None):
    kwargs = {"model": model, "messages": msgs, "stream": True}
    if tools:
        kwargs["tools"] = tools
    if any(x in model.lower() for x in ["gpt-5", "o1", "o3", "gemini-3", "gemini-2"]):
        kwargs["reasoning_effort"] = "medium"
    return kwargs

def handle_stream(stream, get_signature=False):
    buf, t_buf = "", {}
    printed, reasoning_active = False, False
    dots, last_anim = 0, 0
    sig, live = None, None

    try:
        for chunk in stream:
            delta = chunk.choices[0].delta
            
            if get_signature and hasattr(delta, 'extra_content'):
                sig = delta.extra_content.get('google', {}).get('thought_signature', sig)

            if delta.tool_calls or (delta.content is not None):
                reasoning_active = _clear_animation(reasoning_active)

            if delta.tool_calls:
                for tc in delta.tool_calls:
                    idx = tc.index
                    if idx not in t_buf: 
                        t_buf[idx] = {"id": tc.id, "name": tc.function.name, "args": ""}
                    if tc.function.arguments: 
                        t_buf[idx]["args"] += tc.function.arguments
                continue 

            if delta.content is not None:
                buf += delta.content
                if not live:
                    live = Live(_md(buf), console=console, refresh_per_second=15)
                    live.start()
                else:
                    live.update(_md(buf))
                printed = True
                continue 

            has_reasoning = hasattr(delta, 'reasoning_content') and delta.reasoning_content
            if has_reasoning or (not printed and not t_buf and not live):
                reasoning_active, dots, last_anim = _update_animation(reasoning_active, dots, last_anim)
    
    except KeyboardInterrupt:
        buf += "\n\n*[Interrupted]*"
    finally:
        reasoning_active = _clear_animation(reasoning_active)
        if hasattr(stream, 'close'):
            try: stream.close()
            except: pass
        if live:
            live.update(_md(buf))
            live.stop()
        elif buf:
            console.print(_md(buf))
    
    return buf, t_buf, sig

def chat(ai, query, history, model):
    new = [{"role": "user", "content": query}]
    msgs = [{"role": "system", "content": get_sys()}] + history + new
    
    try:
        kwargs1 = build_kwargs(model, msgs, get_conf())
        stream1 = ai.chat.completions.create(**kwargs1)
        
        c_buf, t_buf, sig = handle_stream(stream1, get_signature=True)

        if not t_buf or "*[Interrupted]*" in c_buf:
            new.append({"role": "assistant", "content": c_buf})
            return new
        
        calls = []
        for i, idx in enumerate(sorted(t_buf.keys())):
            call = {
                "id": t_buf[idx]["id"],
                "type": "function",
                "function": {"name": t_buf[idx]["name"], "arguments": t_buf[idx]["args"]}
            }
            if i == 0:
                call["extra_content"] = {"google": {"thought_signature": sig or "skip_thought_signature_validator"}}
            calls.append(call)

        asst_msg = {"role": "assistant", "content": c_buf or None, "tool_calls": calls}
        msgs.append(asst_msg)
        new.append(asst_msg)

        try:
            with ThreadPoolExecutor() as exe:
                results = list(exe.map(run_tool, 
                                       [t["function"]["name"] for t in calls], 
                                       [t["id"] for t in calls], 
                                       [t["function"]["arguments"] for t in calls]))
                for res in results: 
                    msgs.append(res)
                    new.append(res)
        except KeyboardInterrupt:
            new.append({"role": "assistant", "content": "*[Tool execution interrupted]*"})
            return new

        kwargs2 = build_kwargs(model, msgs)
        stream2 = ai.chat.completions.create(**kwargs2)
        
        final_buf, _, _ = handle_stream(stream2)
        
        new.append({"role": "assistant", "content": final_buf})
        return new

    except Exception as e: 
        raise e
