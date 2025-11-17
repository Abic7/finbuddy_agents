# core/hybrid_client.py
# Hybrid LLM client: tries OpenAI first and falls back to a local LM Studio-compatible endpoint.
import json
import os
import sys
import requests
import openai
from openai.error import OpenAIError
from dotenv import load_dotenv

load_dotenv()

# Read configuration from environment, with sensible defaults
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LM_BASE = os.getenv("LM_BASE", "http://192.168.50.230:1234/v1")
LM_MODEL = os.getenv("LM_MODEL", "openai/gpt-oss-20b")
# Optional API key/token for LM Studio (if your server enforces auth)
LM_API_KEY = os.getenv("LM_API_KEY")

if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY


def _lm_probe(timeout=5):
    """
    Probe the LM Studio `/models` endpoint to see if the LM_MODEL is available.
    Returns (ok: bool, message: str).
    """
    try:
        url = LM_BASE.rstrip("/") + "/models"
        headers = {}
        if LM_API_KEY:
            headers["Authorization"] = f"Bearer {LM_API_KEY}"
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
        try:
            data = resp.json()
            text = json.dumps(data)
        except Exception:
            text = resp.text or ""

        if LM_MODEL in text:
            return True, "Model appears in /models response"
        return False, "/models did not list the configured LM_MODEL"
    except Exception as e:
        return False, str(e)


# Perform a quick probe if no OpenAI key is present so users get immediate feedback
if not OPENAI_API_KEY:
    ok, msg = _lm_probe()
    if ok:
        print(f"[HYBRID CLIENT] LM Studio probe succeeded: {msg}")
    else:
        print(f"[HYBRID CLIENT] Warning: LM Studio probe failed: {msg}. "
              "The fallback will still attempt to call LM Studio when needed.")


def generate(prompt, max_tokens=150, temperature=0.7):
    """
    Hybrid LLM client: try OpenAI cloud first (if API key present), then fall back to a
    local LM Studio-compatible endpoint using direct HTTP requests. Returns the model text
    or an error string.
    """
    # --- Try OpenAI cloud ---
    if OPENAI_API_KEY:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4.1-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return response.choices[0].message.content
        except OpenAIError as e:
            print(f"[HYBRID CLIENT] OpenAI error: {e}. Switching to LM Studio fallback...")
        except Exception as e:
            print(f"[HYBRID CLIENT] Unexpected OpenAI error: {e}. Falling back...")

    # --- LM Studio fallback (use requests directly, don't mutate openai globals) ---
    try:
        url = LM_BASE.rstrip("/") + "/chat/completions"
        headers = {"Content-Type": "application/json"}
        if LM_API_KEY:
            headers["Authorization"] = f"Bearer {LM_API_KEY}"

        payload = {
            "model": LM_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        # Extract model text robustly for a few response shapes
        text = None
        if isinstance(data, dict):
            if "choices" in data and isinstance(data["choices"], list) and data["choices"]:
                choice = data["choices"][0]
                if isinstance(choice, dict) and "message" in choice and isinstance(choice["message"], dict):
                    text = choice["message"].get("content")
                elif isinstance(choice, dict) and "text" in choice:
                    text = choice.get("text")
            elif "text" in data:
                text = data.get("text")

        if text is None:
            text = str(data)

        print(f"[HYBRID CLIENT] LM Studio response: {text}")
        if text.strip() == "Returning 200 anyway":
            print("[HYBRID CLIENT] LM Studio returned placeholder. Ending run.")
            sys.exit(1)
        return text.strip()

    except Exception as e:
        print(f"[HYBRID CLIENT] LM Studio error: {e}")
        return "ERROR: No model available."
