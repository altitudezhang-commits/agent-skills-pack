#!/usr/bin/env python3
"""Free no-key LLM for light work.

Primary: local FreeLLMAPI router ($FREELLMAPI_HOME, http://localhost:3001)
with model "auto" -> smart routing across keyless providers (kilo/ovh/Pollinations/...).
The router's unified key is read at runtime from its own sqlite DB (localhost-only,
locally generated single-user key -- not a user credential, never stored in files).
Fallback chain: 1) local router -> 2) Gemini (gemini-3.8-flash) via stored Secure
a vault-stored Gemini credential (surrogate, key never exposed) ->
3) direct Pollinations anonymous endpoint.

Usage:
    freellm.py [--system SYS] [--max-tokens N] [--temperature T] [--model M] [PROMPT]
    freellm.py --models
Prompt comes from argv, or stdin when argv is empty.
Prints assistant text to stdout; errors go to stderr with non-zero exit.
"""
import json
import os
import sqlite3
import sys
import urllib.request
import urllib.error

# Default model: pollinations-openai via the local router (verified 2026-10-14:
# clean Chinese output, ~4s). "auto" picks whatever is fastest, which is often a
# reasoning-distilled model that leaks its chain-of-thought into the answer.
DEFAULT_MODEL = "pollinations-openai"
POLL_BASE = "https://text.pollinations.ai"
LOCAL_BASE = "http://localhost:3001"
LOCAL_DB = os.environ.get("FREELLMAPI_DB", os.path.expanduser("~/freellmapi/server/data/freeapi.db"))
TIMEOUT = 120


def local_uak():
    """Read the router's unified key from its own DB. None if unavailable."""
    try:
        con = sqlite3.connect(LOCAL_DB, timeout=5)
        row = con.execute(
            "SELECT value FROM settings WHERE key='unified_api_key'").fetchone()
        con.close()
        return row[0] if row else None
    except Exception:
        return None


def api_post(base, path, payload, api_key=None):
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    req = urllib.request.Request(
        base + path,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")[:500]
        raise RuntimeError(f"HTTP {e.code}: {body}")
    except Exception as e:
        raise RuntimeError(f"request failed: {e}")


def strip_ad(text):
    """Pollinations anonymous tier appends a support/ad footer; drop it."""
    for marker in ("**Support Pollinations.AI:**", "\U0001f338 **Ad** \U0001f338"):
        idx = text.find(marker)
        if idx != -1:
            text = text[:idx]
    lines = text.rstrip().split("\n")
    while lines and lines[-1].strip() in ("---", "***", "___"):
        lines.pop()
    return "\n".join(lines).rstrip()


def extract_text(data):
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        raise RuntimeError(f"unexpected response: {json.dumps(data)[:300]}")


GEMINI_HELPER = os.path.expanduser(
    os.environ.get("GEMINI_CHAT_PATH", "gemini_chat.py"))


def gemini_chat(prompt, system=None, max_tokens=600, temperature=0.7):
    """Third fallback: Gemini (gemini-3.8-flash) via the stored Secure Vault
    a vault-stored credential. The key never leaves the vault: the
    helper uses a surrogate swapped in by the runtime on the approved request.
    Free-tier data may be used by Google, so light work only."""
    import subprocess
    if not os.path.isfile(GEMINI_HELPER):
        raise RuntimeError("gemini helper not installed")
    cmd = [sys.executable, GEMINI_HELPER, "--max-tokens", str(max_tokens),
           "--temperature", str(temperature)]
    if system:
        cmd += ["--system", system]
    cmd.append(prompt)
    env = {k: v for k, v in os.environ.items()
           if k not in ("no_proxy", "NO_PROXY")}
    try:
        p = subprocess.run(cmd, capture_output=True, text=True,
                           timeout=TIMEOUT, env=env)
    except Exception as e:
        raise RuntimeError(f"gemini helper failed: {e}")
    if p.returncode != 0:
        raise RuntimeError(f"gemini helper failed: {p.stderr.strip()[:300]}")
    out = p.stdout.strip()
    if not out:
        raise RuntimeError("gemini helper returned empty")
    return out


def chat(prompt, system=None, model="auto", max_tokens=600, temperature=0.7):
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    payload = {"model": model, "messages": messages,
               "max_tokens": max_tokens, "temperature": temperature}
    # 1) local router first
    uak = local_uak()
    if uak:
        try:
            data = api_post(LOCAL_BASE, "/v1/chat/completions", payload, api_key=uak)
            return strip_ad(extract_text(data))
        except RuntimeError as e:
            print(f"[freellm] local router failed ({e}), falling back to Gemini",
                  file=sys.stderr)
    # 2) Gemini fallback via stored vault credential (added 2026-10-20)
    try:
        return gemini_chat(prompt, system=system, max_tokens=max_tokens,
                           temperature=temperature)
    except RuntimeError as e:
        print(f"[freellm] gemini fallback failed ({e}), falling back to Pollinations",
              file=sys.stderr)
    # 3) direct Pollinations fallback (model alias differs there)
    fb_model = "openai" if model in ("auto", DEFAULT_MODEL) else model
    data = api_post(POLL_BASE, "/openai", dict(payload, model=fb_model))
    return strip_ad(extract_text(data))


def list_models():
    uak = local_uak()
    if uak:
        try:
            req = urllib.request.Request(
                LOCAL_BASE + "/v1/models",
                headers={"Authorization": f"Bearer {uak}"}, method="GET")
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.load(resp)
            for m in data.get("data", []):
                print(m.get("id"))
            return
        except Exception as e:
            print(f"[freellm] local router failed ({e}), falling back", file=sys.stderr)
    req = urllib.request.Request(POLL_BASE + "/models", method="GET")
    with urllib.request.urlopen(req, timeout=30) as resp:
        models = json.load(resp)
    for m in models:
        print(f"{m.get('name')} | {m.get('tier')} | {m.get('description', '')[:70]}")


def main(argv):
    if "--models" in argv:
        list_models()
        return 0
    system, model, max_tokens, temperature = None, DEFAULT_MODEL, 600, 0.7
    prompt_parts = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--system" and i + 1 < len(argv):
            system = argv[i + 1]; i += 2
        elif a == "--model" and i + 1 < len(argv):
            model = argv[i + 1]; i += 2
        elif a == "--max-tokens" and i + 1 < len(argv):
            max_tokens = int(argv[i + 1]); i += 2
        elif a == "--temperature" and i + 1 < len(argv):
            temperature = float(argv[i + 1]); i += 2
        else:
            prompt_parts.append(a); i += 1
    prompt = " ".join(prompt_parts).strip()
    if not prompt:
        prompt = sys.stdin.read().strip()
    if not prompt:
        print("error: empty prompt", file=sys.stderr)
        return 2
    try:
        print(chat(prompt, system=system, model=model,
                   max_tokens=max_tokens, temperature=temperature))
        return 0
    except RuntimeError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
