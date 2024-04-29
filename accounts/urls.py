from django.urls import path  # Importing the path function from django.urls module
# Importing the necessary views
from .views import UserRegisterView, ProfileEditView, PasswordChangeView, password_success, logout_success, AccountEditView

urlpatterns = [
    # Mapping the 'signup/' URL to the UserRegisterView
    path('signup/', UserRegisterView.as_view(), name='signup'),
    # Mapping the 'edit-profile/' URL to the ProfileEditView
    path('edit-profile/', ProfileEditView.as_view(), name='edit-profile'),
    # Mapping the 'edit-account/' URL to the AccountEditView
    path('edit-account/', AccountEditView.as_view(), name='edit-account'),
    # Mapping the 'password/' URL to the PasswordChangeView
    path('password/', PasswordChangeView.as_view(), name='change-password'),
    # Mapping the 'password_success' URL to the password_success function
    path('password_success', password_success, name='password-success'),
    # Mapping the 'logout_success' URL to the logout_success function
    path('logout_success', logout_success, name='logout_success')
]
