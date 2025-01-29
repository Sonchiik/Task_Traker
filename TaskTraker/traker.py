import json
import os
import argparse
from datetime import datetime
from dataclasses import dataclass, asdict

@dataclass
class TaskConfiguration:
    id: int
    description: str
    status: str
    createdAt: str
    updatedAt: str


class Traker:
    def __init__(self) -> None:
        self.filename: str = "task.json"
        
    def add_to_json(self, tasks):
        with open(self.filename, "w") as f:
            json.dump(tasks, f, indent=4, default=str)
                
    
    def read_from_json(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                try:
                    return json.load(f)    
                except json.JSONDecodeError:
                    return []
        return []
                
    def generate_id(self):
        tasks = self.read_from_json()
        if tasks:
            return max(task["id"] for task in tasks) + 1
        return 1
        
    def add(self, description: str, status: str = "Not Done"):
        new_task = TaskConfiguration(
            id = self.generate_id(),
            description = description,
            status = status,
            createdAt = datetime.now().strftime("%Y-%m-%d %H:%M"),
            updatedAt = datetime.now().strftime("%Y-%m-%d %H:%M")
        )
        tasks = self.read_from_json()
        tasks.append(asdict(new_task))
        self.add_to_json(tasks)
        
    def delete(self, id: int):
        tasks = self.read_from_json()
        tasks = [task for task in tasks if task["id"] != id]
        for num, task in enumerate(tasks, start=1):
            task["id"] = num
        self.add_to_json(tasks)
        
    def update(self, id: int, description: str = None, status: str = None):
        tasks = self.read_from_json()
        for task in tasks:
            if task["id"] == id:
                if description:
                    task["description"] = description
                if status is not None:
                    task["status"] = status
                    
                task["updatedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                self.add_to_json(tasks)
                return
            
    def all_tasks(self):
        tasks = self.read_from_json()
        for task in tasks:
            print(f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}, "
                  f"Created At: {task['createdAt']}, Updated At: {task['updatedAt']}")
            
    def done_tasks(self):
        tasks = self.read_from_json()
        tasks = [task for task in tasks if task["status"] == "Done"]
        for task in tasks:
            print(f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}, "
                  f"Created At: {task['createdAt']}, Updated At: {task['updatedAt']}")
    def tasks_in_progress(self):
        tasks = self.read_from_json()
        tasks = [task for task in tasks if task["status"] == "In Progress"]
        for task in tasks:
            print(f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}, "
                  f"Created At: {task['createdAt']}, Updated At: {task['updatedAt']}")
    def not_done_tasks(self):
        tasks = self.read_from_json()
        tasks = [task for task in tasks if task["status"] == "Not Done"]
        for task in tasks:
            print(f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}, "
                  f"Created At: {task['createdAt']}, Updated At: {task['updatedAt']}")
def main():
    parser = argparse.ArgumentParser(description="Task CLI")
    subparser = parser.add_subparsers(dest="command")
    
    subparser.add_parser("list", help="List all tasks")
    subparser.add_parser("done", help="List of done tasks")
    subparser.add_parser("in-progress", help="List of done tasks")
    subparser.add_parser("not-done", help="List of done tasks")
    
    add_parser = subparser.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", type=str, help="Task description")
    
    delete_parser = subparser.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID")
    
    update_parser = subparser.add_parser("update", help="Update a task")
    update_parser.add_argument("id", type=int, help="Task ID")
    update_parser.add_argument("--description", type=str, help="New description")
    update_parser.add_argument("--status", type=str, choices=["Not Done", "In Progress", "Done"], help="New status", default=None)

    
    args = parser.parse_args()
    manager = Traker()
    
    if args.command == "add":
        manager.add(args.description)
    elif args.command == "delete":
        manager.delete(args.id)
    elif args.command == "update":
        manager.update(args.id, description=args.description, status=args.status)
    elif args.command == "list":
        manager.all_tasks()
    elif args.command == "done":
        manager.done_tasks()
    elif args.command == "in-progress":
        manager.tasks_in_progress()
    elif args.command == "not-done":
        manager.not_done_tasks()
        
        
if __name__ == "__main__":
    main()