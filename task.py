from datetime import datetime

class Task:

    """
    A single task with the required attributes.
    """

    def __init__(self, title, description='', due_date=None, priority_level='Low', status='Pending', created_at=None, task_id=None):
        self.__task_id = task_id
        self.__title = title
        self.__description = description
        self.__due_date = due_date if due_date else datetime.now()
        self.__priority_level = priority_level
        self.__status = status
        self.__created_at = created_at or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Getters for encapsulation

    def get_id(self):
        return self.__task_id

    def get_title(self):
        return self.__title

    def get_description(self):
        return self.__description

    def get_due_date(self):
        return self.__due_date

    def get_priority(self):
        return self.__priority_level

    def get_status(self):
        return self.__status

    def get_created_at(self):
        return self.__created_at
    
    # Setters for encapsulation

    def set_title(self, title):
        self.__title = title

    def set_description(self, description):
        self.__description = description

    def set_due_date(self, due_date):
        self.__due_date = due_date

    def set_priority(self, priority):
        if priority not in ['Low', 'Medium', 'High']:
            raise ValueError("Priority must be Low, Medium, or High.")
        self.__priority_level = priority

    def set_status(self, status):
        if status not in ['Pending', 'In Progress', 'Completed']:
            raise ValueError("Status must be Pending, In Progress, or Completed.")
        self.__status = status


    """
        String for CLI output.
    """
    
    def __str__(self):
        
        return (
            f"[ID: {self.get_id()}] {self.get_title()} | "
            f"Due: {self.get_due_date()} | "
            f"Priority: {self.get_priority()} | "
            f"Status: {self.get_status()}"
        )