import json
import os
from datetime import datetime

# Path to store log history
HISTORY_FILE = "logs/history.json"

def log_analysis(data: dict):
    # Ensure the logs directory exists
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)

    # Load existing history or start a new list
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []
    else:
        history = []

    # Add timestamp and log entry
    entry = {
        "timestamp": datetime.now().isoformat(),
        **data
    }
    history.append(entry)

    # Write to file in human-readable format (unicode characters preserved)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

def log_feedback(entry_index: int, feedback_type: str, comments: str = ""):
    """
    Updates a specific log entry with user feedback.
    """
    if not os.path.exists(HISTORY_FILE):
        return

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
        
        # Check if index is valid (most recent is usually checking -1, but let's assume index is passed)
        if 0 <= entry_index < len(history):
            history[entry_index]["user_feedback"] = {
                "type": feedback_type,
                "comments": comments,
                "timestamp": datetime.now().isoformat()
            }
            
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
                
    except Exception as e:
        print(f"[ERROR] Failed to log feedback: {e}")
