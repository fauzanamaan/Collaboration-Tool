from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth import password_validation
from .models import Profile

# Importing form classes for user creation, password change, and user change
from django.contrib.auth.models import User  # Importing User model
# Importing password validation functions
from django import forms  # Importing forms module


class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(
        # Email field with form-control class
        attrs={'class': 'form-control'}))
    first_name = forms.CharField(
        # First name field with form-control class
        max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(
        # Last name field with form-control class
        max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2')  # Fields to be displayed in the form

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        # Username field with form-control class
        self.fields['username'].widget.attrs['class'] = 'form-control'
        # Password1 field with form-control class
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        # Password2 field with form-control class
        self.fields['password2'].widget.attrs['class'] = 'form-control'

    def get_password_help_texts(self):
        return password_validation.password_validators_help_texts()


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(
        # Old password field with form-control class and type password
        attrs={'class': 'form-control', 'type': 'password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(
        # New password1 field with form-control class and type password
        attrs={'class': 'form-control', 'type': 'password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(
        # New password2 field with form-control class and type password
        attrs={'class': 'form-control', 'type': 'password'}))

    class Meta:
        model = User
        # Fields to be displayed in the form
        fields = ('old_password', 'new_password1', 'new_password2')


class EditAccountForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(
        # Email field with form-control class
        attrs={'class': 'form-control'}))  # Inline comment for email field
    first_name = forms.CharField(
        # First name field with form-control class
        max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))  # Inline comment for first name field
    last_name = forms.CharField(
        # Last name field with form-control class
        max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))  # Inline comment for last name field
    username = forms.CharField(
        # Username field with form-control class
        max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))  # Inline comment for username field
    last_login = forms.CharField(
        # Last login field with form-control class
        max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))  # Inline comment for last login field
    is_superuser = forms.CharField(
        # Is superuser field with form-check class
        max_length=100, widget=forms.CheckboxInput(attrs={'class': 'form-check'}))  # Inline comment for is superuser field
    is_staff = forms.CharField(
        # Is staff field with form-check class
        max_length=100, widget=forms.CheckboxInput(attrs={'class': 'form-check'}))  # Inline comment for is staff field
    is_active = forms.CharField(
        # Is active field with form-check class
        max_length=100, widget=forms.CheckboxInput(attrs={'class': 'form-check'}))  # Inline comment for is active field
    date_joined = forms.CharField(
        # Date joined field with form-control class
        max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))  # Inline comment for date joined field

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'last_login', 'is_superuser',
                  # Fields to be displayed in the form
                  'is_staff', 'is_active', 'date_joined')  # Inline comment for fields


class ProfilePageForm(forms.ModelForm):
    class Meta:
        model = Profile  # Model for the form
        fields = ('bio', 'profile_pic', 'facebook_url',  # Fields to be displayed in the form
                  'twitter_url', 'instagram_url', 'linkedin_url')
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control'}),  # Bio field with form-control class
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),  # Profile picture field with form-control class
            'facebook_url': forms.TextInput(attrs={'class': 'form-control'}),  # Facebook URL field with form-control class
            'twitter_url': forms.TextInput(attrs={'class': 'form-control'}),  # Twitter URL field with form-control class
            'instagram_url': forms.TextInput(attrs={'class': 'form-control'}),  # Instagram URL field with form-control class
            'linkedin_url': forms.TextInput(attrs={'class': 'form-control'}),  # LinkedIn URL field with form-control class
        }
