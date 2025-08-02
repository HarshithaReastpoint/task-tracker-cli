#!/usr/bin/env python3
import sys
import json
import os
from datetime import datetime

FILE_NAME = "tasks.json"

# ANSI color codes
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# Load tasks from file
def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r") as f:
        return json.load(f)

# Save tasks to file
def save_tasks(tasks):
    with open(FILE_NAME, "w") as f:
        json.dump(tasks, f, indent=2)

# Get current time
def now():
    return datetime.now().isoformat(timespec="seconds")

# Add new task
def add_task(description):
    tasks = load_tasks()
    new_id = max([task["id"] for task in tasks], default=0) + 1
    new_task = {
        "id": new_id,
        "description": description,
        "status": "todo",
        "createdAt": now(),
        "updatedAt": now()
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(Colors.OKGREEN + f"Task added successfully (ID: {new_id})" + Colors.ENDC)

# Update task
def update_task(task_id, new_desc):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = new_desc
            task["updatedAt"] = now()
            save_tasks(tasks)
            print(Colors.OKGREEN + "Task updated successfully." + Colors.ENDC)
            return
    print(Colors.FAIL + "Task not found." + Colors.ENDC)

# Delete task
def delete_task(task_id):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]
    if len(tasks) == len(new_tasks):
        print(Colors.FAIL + "Task not found." + Colors.ENDC)
    else:
        save_tasks(new_tasks)
        print(Colors.OKGREEN + "Task deleted successfully." + Colors.ENDC)

# Mark task
def mark_task(task_id, new_status):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = new_status
            task["updatedAt"] = now()
            save_tasks(tasks)
            print(Colors.OKGREEN + f"Task marked as {new_status}." + Colors.ENDC)
            return
    print(Colors.FAIL + "Task not found." + Colors.ENDC)

# List tasks
def list_tasks(filter_status=None):
    tasks = load_tasks()
    if filter_status:
        tasks = [t for t in tasks if t["status"] == filter_status]
    if not tasks:
        print(Colors.WARNING + "No tasks found." + Colors.ENDC)
    else:
        for task in tasks:
            print(Colors.OKCYAN + f"[{task['id']}] {task['description']} - {task['status']}" + Colors.ENDC)

# Export tasks to text file
def export_tasks():
    tasks = load_tasks()
    if not tasks:
        print(Colors.WARNING + "No tasks to export." + Colors.ENDC)
        return
    with open("tasks_export.txt", "w") as f:
        for task in tasks:
            line = f"[{task['id']}] {task['description']} - {task['status']} (Created: {task['createdAt']})\n"
            f.write(line)
    print(Colors.OKGREEN + "Tasks exported to tasks_export.txt" + Colors.ENDC)

# Main command handler
def main():
    if len(sys.argv) < 2:
        print(Colors.WARNING + "Usage: python task_cli.py <command> [arguments]" + Colors.ENDC)
        return

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print(Colors.FAIL + "Please provide a task description." + Colors.ENDC)
        else:
            add_task(sys.argv[2])

    elif command == "update":
        if len(sys.argv) < 4:
            print(Colors.FAIL + "Usage: update <id> <new description>" + Colors.ENDC)
        else:
            update_task(int(sys.argv[2]), sys.argv[3])

    elif command == "delete":
        if len(sys.argv) < 3:
            print(Colors.FAIL + "Usage: delete <id>" + Colors.ENDC)
        else:
            delete_task(int(sys.argv[2]))

    elif command == "mark-in-progress":
        if len(sys.argv) < 3:
            print(Colors.FAIL + "Usage: mark-in-progress <id>" + Colors.ENDC)
        else:
            mark_task(int(sys.argv[2]), "in-progress")

    elif command == "mark-done":
        if len(sys.argv) < 3:
            print(Colors.FAIL + "Usage: mark-done <id>" + Colors.ENDC)
        else:
            mark_task(int(sys.argv[2]), "done")

    elif command == "list":
        if len(sys.argv) == 3:
            list_tasks(sys.argv[2])
        else:
            list_tasks()

    elif command == "export":
        export_tasks()

    else:
        print(Colors.FAIL + "Unknown command." + Colors.ENDC)

if __name__ == "__main__":
    main()
