import requests
import os

HOST = os.getenv("LM_BASE", "http://localhost:1234/v1")
MODEL = os.getenv("LM_MODEL", "openai/gpt-oss-20b")

# Chat completions (OpenAI-compatible)
url = HOST.rstrip('/') + "/chat/completions"
payload = {"model": MODEL, "messages": [{"role":"user","content":"Hello from test"}]}
r = requests.post(url, json=payload, timeout=15)
print("status:", r.status_code)
print(r.text)