import os
def list_dir(path="."):
    return "\n".join(os.listdir(path))