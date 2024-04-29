# Importing the render function from django.shortcuts module
from django.shortcuts import render
# Importing CreateView and UpdateView classes from django.views.generic module
from django.views.generic import CreateView, UpdateView
# Importing reverse_lazy function from django.urls module
from django.urls import reverse_lazy
# Importing logout function from django.contrib.auth module
from django.contrib.auth import logout
# Importing custom forms from .forms module
from .forms import SignUpForm, PasswordChangingForm, EditAccountForm, ProfilePageForm
# Importing PasswordChangeView class from django.contrib.auth.views module
from django.contrib.auth.views import PasswordChangeView
# Importing LoginRequiredMixin class from django.contrib.auth.mixins module
from django.contrib.auth.mixins import LoginRequiredMixin
# Importing the User model from django.contrib.auth
from django.contrib.auth.models import User

from .models import Profile

def password_success(request):
    # Rendering the password_success.html template
    return render(request, 'registration/password_success.html')


class UserRegisterView(CreateView):
    form_class = SignUpForm  # Assigning SignUpForm class to form_class attribute
    # Assigning 'registration/signup.html' to template_name attribute
    template_name = 'registration/signup.html'
    # Assigning reverse_lazy('login') to success_url attribute
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        # Calling the parent class's get_context_data method
        context = super().get_context_data(**kwargs)
        # Adding password_help_texts to the context dictionary
        context['password_help_texts'] = self.get_form(
        ).get_password_help_texts()
        return context


class AccountEditView(LoginRequiredMixin, UpdateView):
    # Assigning AccountProfileForm class to form_class attribute
    form_class = EditAccountForm
    # Assigning 'registration/account.html' to template_name attribute
    template_name = 'registration/accounts.html'
    # Assigning reverse_lazy('dashboard') to success_url attribute
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        return self.request.user  # Returning the current user object
    

class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'registration/profiles.html'
    fields = ['bio', 'profile_pic', 'facebook_url',
              'twitter_url', 'instagram_url', 'linkedin_url']
    success_url = reverse_lazy('home')

    # Assigning reverse_lazy('dashboard') to success_url attribute
    success_url = reverse_lazy('dashboard')


    def get_object(self):
        # Get or create the Profile object associated with the current user
        Profile.objects.get_or_create(user=self.request.user)
        # Return the Profile object of the current user
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        # Call the parent class's get_context_data method
        context = super().get_context_data(**kwargs)
        # Add the ProfilePageForm instance to the context dictionary
        context['form'] = ProfilePageForm(instance=self.get_object())
        return context

    def form_valid(self, form):
        # Set the user of the form instance to the current user
        form.instance.user = self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class PasswordChangeView(PasswordChangeView):
    # Assigning PasswordChangingForm class to form_class attribute
    form_class = PasswordChangingForm
    # Assigning 'registration/change-password.html' to template_name attribute
    template_name = 'registration/change-password.html'
    # Assigning reverse_lazy('password_success') to success_url attribute
    success_url = reverse_lazy('password_success')


def logout_success(request):
    logout(request)  # Logging out the user
    # Rendering the logout_success.html template
    return render(request, 'registration/logout_success.html')
