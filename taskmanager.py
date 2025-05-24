import json
import os
from datetime import datetime

def logger(func):
    def wrapper(*args, **kwargs):
        print(f"[LOG] Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.tasks = []
        self.filename = filename
        self.load_tasks()

    @logger
    def add_task(self, task, category="General"):
        self.tasks.append({
            "task": task,
            "done": False,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "category": category
        })
        self.save_tasks()
        print("Task added.")

    @logger
    def view_tasks(self):
        if not self.tasks:
            print("No tasks yet.")
            return
        for idx, t in enumerate(self.tasks, 1):
            text = t.get("task") or t.get("title") or "<No description>"
            status = "Done" if t.get("done") else "Not done"
            category = t.get("category", "General")
            timestamp = t.get("timestamp", "N/A")
            print(f"{idx}. [{status}] {text} (Category: {category}, Added: {timestamp})")

    @logger
    def mark_done(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index]["done"] = True
            self.save_tasks()
            print("Task marked as done.")
        else:
            print("Invalid task number.")

    @logger
    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            removed = self.tasks.pop(index)
            text = removed.get("task") or removed.get("title") or "<Unknown>"
            self.save_tasks()
            print(f"Deleted task: '{text}'")
        else:
            print("Invalid task number.")

    @logger
    def view_tasks_by_category(self, category):
        found = False
        for idx, t in enumerate(self.tasks, 1):
            cat = t.get("category", "General")
            if cat.lower() == category.lower():
                found = True
                text = t.get("task") or t.get("title") or "<No description>"
                status = "Done" if t.get("done") else "Not done"
                timestamp = t.get("timestamp", "N/A")
                print(f"{idx}. [{status}] {text} (Added: {timestamp})")
        if not found:
            print(f"No tasks found in category '{category}'.")

    def save_tasks(self):
        with open(self.filename, "w") as f:
            json.dump(self.tasks, f, indent=2)

    def load_tasks(self):
        try:
            with open(self.filename, "r") as f:
                raw = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []
            return

        # Migrate any old entries using "title" ? new "task" key
        migrated = []
        for t in raw:
            if "title" in t and "task" not in t:
                t["task"] = t.pop("title")
                t.setdefault("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                t.setdefault("category", "General")
                t.setdefault("done", False)
            migrated.append(t)
        self.tasks = migrated