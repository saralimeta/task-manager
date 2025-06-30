# task_manager.py

from task import Task
from db import Database
from datetime import datetime
import heapq


class TaskManager:
    """
    Manages task operations: create, list/read, update, completed, delete.
    Interacts with the MySQL database using raw SQL queries.
    """

    def __init__(self, db: Database):
        """
        Initialize with a database connection.
        """
        self.db = db

    def validate_date(self, date_str):
        """
        Validates that a date string is in YYYY-MM-DD format and handles all cases where date
        is not valid. (ex: not a leap year, invalid month, invalid day, etc.)
        """
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def add_task(self, title, description="", due_date=None, priority_level="Low"):
        """
        Adds a new task to the database.
        """
        if not title:
            print("[ERROR] Please input title (required).")
            return

        if due_date and not self.validate_date(due_date):
            print("[ERROR] Due date must be in YYYY-MM-DD format.")
            return

        if priority_level not in ['Low', 'Medium', 'High']:
            print("[ERROR] priority level must be: Low or Medium or High.")
            return

        task = Task(
            title=title,
            description=description,
            due_date=due_date,
            priority_level=priority_level
        )

        query = """
            INSERT INTO tasks (title, description, due_date, priority_level, status, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            task.get_title(),
            task.get_description(),
            task.get_due_date(),
            task.get_priority(),
            task.get_status(),
            task.get_created_at()
        )

        self.db.execute(query, values)
        print("Task added successfully")

    def list_tasks(self, status=None, priority_level=None, due_date=None):
        """
        Lists tasks with optional filtering.

        This method:
            - Retrieves all tasks from the database
            - Applies filtering based on optional parameters:
                * status (e.g., Pending, In Progress, Completed)
                * priority_level (Low, Medium, High)
                * due_date (YYYY-MM-DD format)
            - Performs custom sorting using a priority queue (heapq),
            where tasks are ranked by:
                1. Due date (earlier comes first)
                2. Priority level (High > Medium > Low)

        """

        self.db.cursor.execute("SELECT * FROM tasks")
        rows = self.db.fetchall()
        if not rows:
            print("No tasks found.")
            return
        
        filtered_rows = []

        for row in rows:
            if status and row['status'] != status:
                continue
            if priority_level and row['priority_level'] != priority_level:
                continue
            if due_date:
                if not self.validate_date(due_date):
                    print("[ERROR] Due date must be in YYYY-MM-DD format.")
                    return
                if str(row['due_date']) != due_date:
                    continue
            filtered_rows.append(row)

        if not filtered_rows:
            print("No tasks matched your filters.")
            return

        priority_score = {"High": 3, "Medium": 2, "Low": 1}
        heap = []

        for row in filtered_rows:
            due = row['due_date'] or datetime.max.date()  
            score = priority_score.get(row['priority_level'], 1)
            heapq.heappush(heap, (due, -score, row))  # Sort: earlier date, higher priority
        
        while heap:
            _, _, row = heapq.heappop(heap)

            task = Task(
                task_id=row['task_id'],
                title=row['title'],
                description=row['description'],
                due_date=row['due_date'],
                priority_level=row['priority_level'],
                status=row['status'],
                created_at=row['created_at']
            )

            print(task)

    def update_task(self, task_id, title=None, description=None, due_date=None, priority_level=None, status=None):
        """
        Updates a task's details by ID (Execute list method to determine task ID).
        """

        self.db.cursor.execute("SELECT * FROM tasks WHERE task_id = %s", (task_id,))
        row = self.db.fetchone()

        if not row:
            print(f"[ERROR] No task found with ID {task_id}.")
            return
        task = Task(
            task_id=row['task_id'],
            title=row['title'],
            description=row['description'],
            due_date=row['due_date'],
            priority_level=row['priority_level'],
            status=row['status'],
            created_at=row['created_at']
        )

        try:
            if title:
                task.set_title(title)
            if description:
                task.set_description(description)
            if due_date:
                if not self.validate_date(due_date):
                    print("[ERROR] Due date must be in YYYY-MM-DD format.")
                    return
                task.set_due_date(due_date)
            if priority_level:
                task.set_priority(priority_level)
            if status:
                task.set_status(status)
        except ValueError as e:
            print(f"[ERROR] {e}")
            return

        query = """
        UPDATE tasks
        SET title = %s,
            description = %s,
            due_date = %s,
            priority_level = %s,
            status = %s
        WHERE task_id = %s
    """
        values = (
            task.get_title(),
            task.get_description(),
            task.get_due_date(),
            task.get_priority(),
            task.get_status(),
            task.get_id()
        )

        success = self.db.execute(query, values)
        if success:
            print("Task updated successfully")
        else:
            print("[ERROR] Task update failed.")

    def complete_task(self, task_id):
        """
        Marks a task as completed by task_id.
        """
        self.db.cursor.execute("SELECT * FROM tasks WHERE task_id = %s", (task_id,))
        row = self.db.fetchone()

        if not row:
            print(f"[ERROR] No task found with ID {task_id}.")
            return

        task = Task(
            task_id=row['task_id'],
            title=row['title'],
            description=row['description'],
            due_date=row['due_date'],
            priority_level=row['priority_level'],
            status=row['status'],
            created_at=row['created_at']
        )

        try:
            task.set_status("Completed") 
        except ValueError as e:
            print(f"[ERROR] {e}")
            return

        query = "UPDATE tasks SET status = %s WHERE task_id = %s"
        values = (task.get_status(), task.get_id())

        success = self.db.execute(query, values)
        if success:
            print("Task marked as completed!")
        else:
            print("[ERROR] Failed to complete task.")

    def delete_task(self, task_id):
        """
        Deletes a task by ID.
        """
        query = "DELETE FROM tasks WHERE task_id = %s"
        self.db.execute(query, (task_id,))
        print("Task deleted successfully!")
