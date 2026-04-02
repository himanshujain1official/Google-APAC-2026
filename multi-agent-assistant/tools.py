import sqlite3

# --- TASK MANAGEMENT TOOLS ---
def add_task(task_name: str, due_date: str) -> str:
    """Adds a new task to the task manager."""
    conn = sqlite3.connect('assistant.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (task_name, due_date) VALUES (?, ?)", (task_name, due_date))
    conn.commit()
    conn.close()
    return f"Success: Task '{task_name}' added for {due_date}."

def get_pending_tasks() -> str:
    """Retrieves all pending tasks from the task manager."""
    conn = sqlite3.connect('assistant.db')
    cursor = conn.cursor()
    cursor.execute("SELECT task_name, due_date FROM tasks WHERE status='pending'")
    tasks = cursor.fetchall()
    conn.close()
    
    if not tasks:
        return "No pending tasks."
    
    result = "Pending Tasks:\n"
    for t in tasks:
        result += f"- {t[0]} (Due: {t[1]})\n"
    return result

# --- NOTES MANAGEMENT TOOLS ---
def save_note(topic: str, content: str) -> str:
    """Saves a note or summary to the notes database."""
    conn = sqlite3.connect('assistant.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (topic, content) VALUES (?, ?)", (topic, content))
    conn.commit()
    conn.close()
    return f"Success: Note saved under topic '{topic}'."