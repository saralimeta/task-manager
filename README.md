# Task Manager CLI Application

A command-line Task Management system built with Python and MySQL to demonstrate core backend development skills including:

- Object-Oriented Programming (OOP)
- Database interaction
- Custom sorting and filtering logic
- CLI handling with `argparse`
- Input validation and error handling

---

## ⚙️ Features

- ✅ Add new tasks (with title, description, due date, priority)
- ✅ List tasks with optional filtering (by status, priority, or due date)
- ✅ Custom sorting: due date (ASC) and priority (High > Low) using heapq
- ✅ Update task fields
- ✅ Mark tasks as completed
- ✅ Delete tasks

---

## 🛠️ Tech Stack

- Python
- MySQL

---

## 🧪 Setup Instructions

### 1. Install Python Dependencies

```bash
pip install mysql-connector-python
```

### 2. Install Python Dependencies

Open your MYSQL terminal or GUI then copy and run the SQL script under schema.sql

### 3. Change your DB input

In the config.py file, change your DB requirements

## Available Commands

The Task Manager supports the following command-line operations:

---

### `add` — Add a New Task

Create a new task in the system.

**Arguments:**

- `--title` _(required)_ – Name of the task
- `--description` _(optional)_ – Additional details
- `--due_date` _(optional)_ – Due date in `YYYY-MM-DD` format
- `--priority` _(optional)_ – Priority level: `Low`, `Medium`, or `High`

**Example:**

```bash
python main.py add --title "Finish Homework" --description "Math and Science" --due_date 2025-07-03 --priority Medium
```

### `list` — List All Tasks

Display tasks stored in the system, with optional filtering and automatic sorting.

**Optional Filters:**

- `--status` – Filter by status: `Pending`, `In Progress`, or `Completed`
- `--priority` – Filter by priority: `Low`, `Medium`, or `High`
- `--due_date` – Filter by due date in `YYYY-MM-DD` format

**Automatic Sorting:**

- Tasks are sorted first by earliest **due date**, then by **priority** (High > Medium > Low)

**Example:**

```bash
python main.py list --priority High --status "Pending"
```

### `update` — Modify an Existing Task

Update the details of an existing task using its task ID.

**Arguments:**

- `--id` _(required)_ – ID of the task to update
- `--title` _(optional)_ – New title for the task
- `--description` _(optional)_ – Updated task description
- `--due_date` _(optional)_ – New due date in `YYYY-MM-DD` format
- `--priority` _(optional)_ – Updated priority: `Low`, `Medium`, or `High`
- `--status` _(optional)_ – Updated status: `Pending`, `In Progress`, or `Completed`

**Example:**

```bash
python main.py update --id 1 --title "Updated Title" --priority Low
```

### `complete` — Mark a Task as Completed

Change the status of a task to `Completed` using its ID.

**Arguments:**

- `--id` _(required)_ – ID of the task to mark as completed

**Example:**

```bash
python main.py complete --id 1
```

### `delete` — Remove a Task

Permanently delete a task from the database using its ID.

> This action is irreversible. Deleted tasks cannot be recovered.

**Arguments:**

- `--id` _(required)_ – ID of the task to delete

**Example:**

```bash
python main.py delete --id 1
```
