import json
import os
from datetime import datetime
from livekit.agents import function_tool

MEMORY_FILE = os.path.join(os.path.dirname(__file__), "conversations.json")

def _load_all():
    if not os.path.exists(MEMORY_FILE):
        return []
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def _save_all(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@function_tool()
async def load_memory() -> str:
    """Load and return all stored memory entries as text."""
    data = _load_all()
    if not data:
        return "No memory entries found."
    return json.dumps(data, ensure_ascii=False)


@function_tool()
async def save_memory(user_text: str, assistant_text: str = "") -> str:
    """Save a conversation entry (user message and assistant reply) to memory."""
    data = _load_all()
    entry = {
        "user": user_text,
        "assistant": assistant_text,
        "timestamp": datetime.now().isoformat()
    }
    data.append(entry)
    _save_all(data)
    return "Memory saved."


@function_tool()
async def add_memory_entry(user_text: str, assistant_text: str = "") -> str:
    """Add a new conversation entry to memory (user input and assistant response)."""
    data = _load_all()
    entry = {
        "user": user_text,
        "assistant": assistant_text,
        "timestamp": datetime.now().isoformat()
    }
    data.append(entry)
    _save_all(data)
    return "Entry added to memory."


@function_tool()
async def get_recent_conversations(limit: int = 10) -> str:
    """Return a text summary of the most recent conversations from memory."""
    data = _load_all()
    recent = data[-limit:] if data else []
    if not recent:
        return "No previous conversations found."

    lines = []
    for item in recent:
        user = item.get("user", "")
        assistant = item.get("assistant", "")
        lines.append(f"User: {user}\nJarvis: {assistant}")

    return "\n\n".join(lines)