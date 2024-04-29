from django.db import models  # Importing the models module from Django
# Importing the User model from Django's auth module
from django.contrib.auth.models import User
# Importing the merge_sort function from the sorting module
from .sorting import merge_sort

# To-Do List Model


class Task(models.Model):
    priority_scale = {
        'Low': 0,
        'Medium': 1,
        'High': 2,
        'Urgent': 3
    }

    # Creating a foreign key relationship with the User model
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Creating a CharField for the title of the task
    title = models.CharField(max_length=200)
    # Creating a BooleanField to track if the task is completed or not
    completed = models.BooleanField(default=False)
    # Creating a DateTimeField to store the creation date and time of the task
    created = models.DateTimeField(auto_now_add=True)
    # Creating a DateTimeField to store the deadline of the task
    deadline = models.DateTimeField(null=True, blank=True)
    priority = models.IntegerField(
        # Creating an IntegerField to represent the priority of the task
        default=0, choices=[(v, k) for k, v in priority_scale.items()])

    def __str__(self):
        return self.title  # Returning the title of the task as a string representation
