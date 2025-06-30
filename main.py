# main.py

import argparse
from db import Database
from task_manager import TaskManager
from config import DB_CONFIG


def main():
    db = Database(**DB_CONFIG)
    manager = TaskManager(db)

    parser = argparse.ArgumentParser(description="Task Manager CLI")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add Task
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("--title", required=True, help="Task title")
    add_parser.add_argument("--description", help="Task description")
    add_parser.add_argument("--due_date", help="Due date (YYYY-MM-DD)")
    add_parser.add_argument("--priority", choices=["Low", "Medium", "High"], default="Low")

    # List
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("--status", choices=["Pending", "In Progress", "Completed"])
    list_parser.add_argument("--priority", choices=["Low", "Medium", "High"])
    list_parser.add_argument("--due_date", help="Filter by due date (YYYY-MM-DD)")

    # Update
    update_parser = subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("--id", type=int, required=True, help="ID of the task to update")
    update_parser.add_argument("--title", help="New title")
    update_parser.add_argument("--description", help="New description")
    update_parser.add_argument("--due_date", help="New due date (YYYY-MM-DD)")
    update_parser.add_argument("--priority", choices=["Low", "Medium", "High"])
    update_parser.add_argument("--status", choices=["Pending", "In Progress", "Completed"])

    # Complete
    complete_parser = subparsers.add_parser("complete", help="Mark a task as completed")
    complete_parser.add_argument("--id", type=int, required=True, help="ID of the task to complete")

    # Delete
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("--id", type=int, required=True, help="ID of the task to delete")

    args = parser.parse_args()

    if args.command == "add":
        manager.add_task(
            title=args.title,
            description=args.description or "",
            due_date=args.due_date,
            priority_level=args.priority
        )

    elif args.command == "list":
        manager.list_tasks(
            status=args.status,
            priority_level=args.priority,
            due_date=args.due_date
        )

    elif args.command == "update":
        manager.update_task(
            task_id=args.id,
            title=args.title,
            description=args.description,
            due_date=args.due_date,
            priority_level=args.priority,
            status=args.status
        )

    elif args.command == "complete":
        manager.complete_task(task_id=args.id)

    elif args.command == "delete":
        manager.delete_task(task_id=args.id)

    db.close()


if __name__ == "__main__":
    main()
