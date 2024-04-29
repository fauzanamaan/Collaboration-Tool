from django import forms  # Importing the forms module from Django
from .models import Task  # Importing the Task model from the current directory


class TaskForm(forms.ModelForm):
    PRIORITY_CHOICES = [
        (0, 'Low'),  # Priority choice: Low
        (1, 'Medium'),  # Priority choice: Medium
        (2, 'High'),  # Priority choice: High
        (3, 'Urgent')  # Priority choice: Urgent
    ]

    title = forms.CharField(widget=forms.TextInput(
        # Creating a CharField for the title with a TextInput widget
        attrs={'class': 'form-control'}))
    priority = forms.ChoiceField(
        # Creating a ChoiceField for the priority with a Select widget
        choices=PRIORITY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    deadline = forms.DateTimeField(
        # Creating a DateTimeField for the deadline with a DateTimeInput widget
        widget=forms.DateTimeInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Task  # Setting the model for the form to Task
        # Specifying the fields to include in the form
        fields = ['title', 'priority', 'deadline']
