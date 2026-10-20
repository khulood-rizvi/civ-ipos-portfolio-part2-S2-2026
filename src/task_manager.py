from datetime import datetime

from rich.console import Console
from rich.table import Table

from src.file_handler import save_tasks
from src.task import Task

console = Console()


def add_task(tasks, title, description, due_date):
    """
    Add a new task to the task list.

    Args:
        tasks (list): The list of existing Task objects.
        title (str): The title of the new task.
        description (str): A brief description of the task.
        due_date (str): The due date of the task in 'DD-MM-YYYY' format.

    Returns:
        bool: True if the task is added successfully, False otherwise.

    Raises:
        ValueError: If the due date is not in the correct format.

    Side Effects:
        - Saves the updated task list to a file using `save_tasks`.
    """

    # Prevent duplicate tasks
    # Bug #25: Title Validation Ignores Case and Leading/Trailing
    # Whitespace, Allowing Duplicate Titles
    title = title.strip()

    if any(task.title.lower() == title.lower() for task in tasks):
        print("Error: A task with this title already exists.")
        return False

    # Validate due date format
    try:
        datetime.strptime(due_date, "%d-%m-%Y")

    except ValueError:
        print("Error: Invalid date format. Use DD-MM-YYYY.")
        return False

    tasks.append(Task(title, description, due_date))
    save_tasks(tasks)
    return True


def delete_task(tasks, title):
    """
    Delete a task from the task list based on its title.

    Args:
        tasks (list): The list of existing Task objects.
        title (str): The title of the task to be deleted.

    Returns:
        bool: True if the task was found and deleted, False otherwise.

    Side Effects:
        - Saves the updated task list to a file using `save_tasks`.
    """

    title = title.strip()

    for task in tasks:
        # Bug #25: Title Validation Ignores Case and Leading/Trailing
        # Whitespace, Allowing Duplicate Titles
        # Fix: storing titles as it is but comparing by converting into
        # lowercase
        if task.title.lower() == title.lower():
            tasks.remove(task)
            save_tasks(tasks)
            return True

    return False


def list_tasks(tasks, status=None):
    """
    Display tasks in tabular form, optionally filtered by status.
    Headers are Title , DEscription, Status and Due date


    Args:
        tasks (list): The list of existing Task objects.
        status (str, optional): The status to filter tasks by
            (e.g., "pending" or "completed").

    Returns:
        None

    Side Effects:
        - Prints the list of tasks to the console in tabular format.
    """

    if not status:
        filtered = tasks
    else:
        filtered = []

        for task in tasks:
            if task.status == status:
                filtered.append(task)

    if not filtered:
        print("No tasks found.")
        return

    table = Table(
        show_header=True,
        show_lines=True,
        header_style="bold white on dark_blue",
    )

    table.add_column(
        "Title",
        justify="center"

    )
    table.add_column(
        "Description",
        justify="left"
    )
    table.add_column(
        "Status",
        justify="left"
    )
    table.add_column(
        "Due Date",
        width=12,
        justify="right",

    )

    for task in filtered:
        table.add_row(
            task.title,
            task.description,
            task.status,
            task.due_date,
        )

    console.print(table)


def filter_tasks_by_status(tasks, status):
    """
    Filter tasks by their status.

    Args:
        tasks (list): The list of existing Task objects.
        status (str): The status to filter tasks by
            (e.g., "pending" or "completed").

    Returns:
        list: A list of Task objects that match the specified status.
    """

    return [task for task in tasks if task.status == status]
