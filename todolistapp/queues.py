# Importing the connection module from Django's database library
from django.db import connection
from .models import Task  # Importing the Task model from the current package
from django.contrib.auth.models import User


class SortingAlgorithms:
    @staticmethod
    def merge_sort(queue):
        def merge(left, right):
            result = []
            i = j = 0
            while i < len(left) and j < len(right):
                if left[i].get_priority() >= right[j].get_priority():
                    # Append the element from the left list
                    result.append(left[i])
                    i += 1
                else:
                    # Append the element from the right list
                    result.append(right[j])
                    j += 1
            # Append the remaining elements from the left list
            result.extend(left[i:])
            # Append the remaining elements from the right list
            result.extend(right[j:])
            return result

        def divide(queue):
            if len(queue) <= 1:
                return queue
            mid = len(queue) // 2
            # Recursively divide the left half of the queue
            left = divide(queue[:mid])
            # Recursively divide the right half of the queue
            right = divide(queue[mid:])
            return merge(left, right)  # Merge the divided lists

        # Update the queue with the sorted elements
        queue.queue = divide(queue.queue)

    @staticmethod
    def bubble_sort(queue):
        n = len(queue.queue)
        for i in range(n - 1):
            for j in range(n - i - 1):
                if queue.queue[j].get_priority() < queue.queue[j + 1].get_priority():
                    # Swap the elements if they are out of order
                    queue.queue[j], queue.queue[j +
                                                1] = queue.queue[j + 1], queue.queue[j]

    @staticmethod
    def choose_sorting_algorithm(queue):
        if len(queue.queue) <= 10:
            # Use bubble sort for small queues
            SortingAlgorithms.bubble_sort(queue)
        else:
            # Use merge sort for large queues
            SortingAlgorithms.merge_sort(queue)


class TaskNode():
    """A node in a linked list"""

    def __init__(self, task):
        self.task = task
        self.next = None

    def get_task(self):
        return self.task

    def get_priority(self):
        return self.task.priority

    def get_next(self):
        return self.next

    def set_next(self, new_next):
        self.next = new_next

    def __str__(self):
        return f'TaskNode({self.task.name})'


class TaskPriorityQueue():
    """A priority queue stored as a linked list for tasks"""

    def __init__(self, user):
        self.front = None
        self.rear = None
        self.queue = []  # Initializing an empty list to store the task nodes
        self.pointer_index = 0
        self.user = user
        self.load_tasks_from_db()  # Loading tasks from the database


    def load_tasks_from_db(self):
        """Load tasks from the database and add them to the queue"""
        tasks = Task.objects.raw(
            'SELECT * FROM todolistapp_task WHERE user_id = %s', [self.user.id])
        for task in tasks:
            self.add_task(task)  # Adding each task to the queue

    def save_tasks_to_db(self):
        """Delete all tasks from the database and then save tasks from the queue to the database"""
        Task.objects.filter(user=self.user).delete(
        )  # Deleting tasks from the database for the given user
        for task_node in self.queue:
            task_node.get_task().save()  # Saving each task from the queue to the database

    def is_empty(self):
        """Check if the queue is empty"""
        return self.front is None

    def add_task(self, task):
        print("Queues before adding a task", self.queue)
        """Add a task based on the priority"""
        if task.user != self.user:
            return

        new_node = TaskNode(task)  # Creating a new node with the given task
        self.queue.append(new_node)  # Adding the new node to the queue list

        if self.is_empty():
            self.front = new_node
            self.rear = new_node
        else:
            if new_node.get_priority() > self.front.get_priority():
                new_node.set_next(self.front)
                self.front = new_node
            elif new_node.get_priority() <= self.rear.get_priority():
                self.rear.set_next(new_node)
                self.rear = new_node
            else:
                current = self.front
                while current.get_priority() >= new_node.get_priority():
                    previous = current
                    current = current.get_next()
                new_node.set_next(current)
                previous.set_next(new_node)
        self.save_tasks_to_db()  # Saving tasks to the database after adding a new task
        print("Queues after adding a task", self.queue)

    def remove_task_by_id(self, task_id):
        """Remove a task from the queue by its id"""
        self.queue = [
            node for node in self.queue if node.get_task().id != task_id and node.get_task().user == self.user]
        if self.queue:
            self.front = self.queue[0]
            self.rear = self.queue[-1]
        else:
            self.front = None
            self.rear = None

    def sort_queue(self):
        SortingAlgorithms.choose_sorting_algorithm(self)

    def update_pointer(self):
        while self.pointer_index < len(self.queue) and self.queue[self.pointer_index].get_priority() == self.queue[0].get_priority():
            self.pointer_index += 1
