import json
import sys
import os

# === Setup paths ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

TASKS_FILE = os.path.join(DATA_DIR, "tasks.json")

def load_tasks():
    """Load tasks from the JSON file, initialize if needed."""
    if not os.path.exists(TASKS_FILE):
        # Create file with empty list
        with open(TASKS_FILE, "w") as file:
            json.dump([], file)
        return []

    with open(TASKS_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            # If file is empty or corrupted
            return []

def save_tasks(tasks):
    """Save tasks to the JSON file."""
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

def add_task(task_description):
    tasks = load_tasks()
    tasks.append({"task": task_description, "completed": False})
    save_tasks(tasks)
    print(f"✅ Task added: {task_description}")

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("📭 No tasks found.")
        return
    for i, task in enumerate(tasks, start=1):
        status = "[X]" if task["completed"] else "[ ]"
        print(f"{i}. {status} {task['task']}")

def complete_task(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks[index]["completed"] = True
        save_tasks(tasks)
        print(f"✅ Task marked as complete: {tasks[index]['task']}")
    else:
        print("❌ Invalid task number.")

def remove_task(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        removed = tasks.pop(index)
        save_tasks(tasks)
        print(f"🗑️ Task removed: {removed['task']}")
    else:
        print("❌ Invalid task number.")

def show_help():
    print("""
📋 TODO CLI - Available Commands:
---------------------------------
python todo.py add "Task Description"      → Add a new task
python todo.py list                        → List all tasks
python todo.py complete [task number]      → Mark task as complete
python todo.py remove [task number]        → Remove a task
""")

def main():
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("❗ Please provide a task description.")
            return
        task_description = " ".join(sys.argv[2:])
        add_task(task_description)

    elif command == "list":
        list_tasks()

    elif command == "complete":
        if len(sys.argv) != 3 or not sys.argv[2].isdigit():
            print("❗ Please provide a valid task number.")
            return
        complete_task(int(sys.argv[2]) - 1)

    elif command == "remove":
        if len(sys.argv) != 3 or not sys.argv[2].isdigit():
            print("❗ Please provide a valid task number.")
            return
        remove_task(int(sys.argv[2]) - 1)

    else:
        show_help()

if __name__ == "__main__":
    main()
