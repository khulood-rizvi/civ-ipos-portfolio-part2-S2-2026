import os
import unittest
from unittest.mock import patch

from src.file_handler import save_tasks, load_tasks
from src.task import Task
from src.task_manager import add_task, delete_task, filter_tasks_by_status, list_tasks

TEST_FILE = "test_tasks.bin"


class TestTaskManager(unittest.TestCase):
    """
    Unit tests for Task Manager functionalities including adding, deleting, filtering,
    and persisting tasks to and from a binary file.
    """

    def setUp(self):
        """
        Set up the test environment by initialising an empty task list
        and backing up the original task binary file.
        """
        self.tasks = []
        self.original_file = "tasks.bin"
        if os.path.exists(TEST_FILE):
            os.remove(TEST_FILE)
        os.rename("tasks.bin", TEST_FILE) if os.path.exists("tasks.bin") else None

    def tearDown(self):
        """
        Clean up the test environment by removing any test-created binary files
        and restoring the original task binary file.
        """
        if os.path.exists("tasks.bin"):
            os.remove("tasks.bin")
        os.rename(TEST_FILE, "tasks.bin") if os.path.exists(TEST_FILE) else None

    def test_add_task(self):
        """
        Test adding a new task to the task list.
        Verify that the task is successfully added and the list size increases.
        """
        result = add_task(self.tasks, "Test Task", "Description", "01-12-2024")
        print(self.tasks[0].description)
        self.assertTrue(result)
        self.assertEqual(len(self.tasks), 1)

    def test_add_duplicate_task(self):
        """
        Test adding a duplicate task with the same title.
        Verify that duplicates are not allowed and the function returns False.
        """
        add_task(self.tasks, "Test1", "Description", "01-12-2021")
        result = add_task(self.tasks, "Test1", "New Description", "02-12-2024")
        self.assertFalse(result)

    @patch("src.task_manager.save_tasks")
    def test_add_duplicate_task_with_whitespace(self, mock_save_tasks):
        """
                Test adding a duplicate task with the same title.
                But 2 titles differ by the addition of leading whitespaces
              Verify that duplicates are not allowed and the function returns False.
               """
        tasks = [Task("Test Task", "Description", "01-12-2024")]

        result2 = add_task(tasks, "  Test Task", "New Description", "02-12-2024")

        self.assertFalse(result2)
        mock_save_tasks.assert_not_called()

    @patch("src.task_manager.save_tasks")
    def test_add_duplicate_task_with_diff_case(self, mock_save_tasks):
        """
        Test adding a duplicate task with the same title.
        Title 1 : task1
        Title 2: TASK1
        Verify that duplicates are not allowed and the function returns False.
        """
        tasks = [Task("Task1", "Description", "01-12-2024")]
        result = add_task(tasks, "TASK1", "New Description", "02-12-2024")
        self.assertFalse(result)
        mock_save_tasks.assert_not_called()

    def test_add_invalid_due_date(self):
        """
        Test adding a task with an invalid due date format.
        Verify that the function handles invalid input gracefully and returns False.
        """
        result = add_task(self.tasks, "Test Task", "Description", "2024-12-01")
        self.assertFalse(result)

    def test_delete_task(self):
        """
        Test deleting a task by its title.
        Verify that the task is removed from the list and the list size decreases.
        """
        add_task(self.tasks, "Task to Delete", "Description", "01-12-2024")
        result = delete_task(self.tasks, "Task to Delete")
        self.assertTrue(result)
        self.assertEqual(len(self.tasks), 0)

    def test_filter_tasks_by_status(self):
        """
        Test filtering tasks based on their status (e.g., 'completed').
        Verify that only tasks matching the specified status are returned.
        """
        task1 = Task("Task 1", "Desc", "01-12-2024", "pending")
        task2 = Task("Task 2", "Desc", "02-12-2024", "completed")
        self.tasks.extend([task1, task2])
        save_tasks(self.tasks)

        filtered = filter_tasks_by_status(self.tasks, "completed")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].title, "Task 2")

    def test_save_and_load_tasks(self):
        """
        Test saving tasks to a file and loading them back.
        Verify that the saved tasks are correctly loaded with the same data.
        """
        add_task(self.tasks, "Persistent Task", "Description", "01-12-2024")
        save_tasks(self.tasks)
        loaded_tasks = load_tasks()
        self.assertEqual(len(loaded_tasks), 1)
        self.assertEqual(loaded_tasks[0].title, "Persistent Task")

    @patch("src.task_manager.console")
    def test_task_list_rich(self, mock_console):
        """
           Test that list_tasks displays tasks using a Rich table.

           Verify that the Rich console's print() method is called
           once when a task list is displayed.
           """
        tasks = [Task("Mock test", "Description", "12-12-2024")]

        # save_tasks(tasks)
        list_tasks(tasks)
        mock_console.print.assert_called_once()


if __name__ == "__main__":
    unittest.main()
