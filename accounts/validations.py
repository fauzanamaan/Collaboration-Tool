import re  # Importing the 're' module for regular expressions
# Importing the 'ValidationError' class from 'django.core.exceptions'
from django.core.exceptions import ValidationError
# Importing the 'gettext' function from 'django.utils.translation'
from django.utils.translation import gettext as _


class BaseValidator:  # Defining a base class called 'BaseValidator'
    # Defining a method called 'validate' that takes 'password' and 'user' as parameters
    def validate(self, password, user=None):
        # Raising a 'NotImplementedError' to indicate that this method must be implemented by subclasses
        raise NotImplementedError

    def get_help_text(self):  # Defining a method called 'get_help_text'
        # Raising a 'NotImplementedError' to indicate that this method must be implemented by subclasses
        raise NotImplementedError


# Defining a subclass called 'UppercaseValidator' that inherits from 'BaseValidator'
class UppercaseValidator(BaseValidator):
    def validate(self, password, user=None):  # Implementing the 'validate' method
        # Checking if the password contains at least one uppercase letter using a regular expression
        if not re.search(r'[A-Z]', password):
            raise ValidationError(  # Raising a 'ValidationError' with a message if the condition is not met
                "The password must contain at least one uppercase letter.")

    def get_help_text(self):  # Implementing the 'get_help_text' method
        return _(  # Returning a translated string using the 'gettext' function
            "Your password must contain at least one uppercase letter."
        )


# Defining a subclass called 'LowercaseValidator' that inherits from 'BaseValidator'
class LowercaseValidator(BaseValidator):
    def validate(self, password, user=None):  # Implementing the 'validate' method
        # Checking if the password contains at least one lowercase letter using a regular expression
        if not re.search(r'[a-z]', password):
            raise ValidationError(  # Raising a 'ValidationError' with a message if the condition is not met
                "The password must contain at least one lowercase letter.")

    def get_help_text(self):  # Implementing the 'get_help_text' method
        return _(  # Returning a translated string using the 'gettext' function
            "Your password must contain at least one lowercase letter."
        )


# Defining a subclass called 'SymbolValidator' that inherits from 'BaseValidator'
class SymbolValidator(BaseValidator):
    def validate(self, password, user=None):  # Implementing the 'validate' method
        # Checking if the password contains at least one symbol using a regular expression
        if not re.search(r'[!@#$%^&*()_+]', password):
            raise ValidationError(  # Raising a 'ValidationError' with a message if the condition is not met
                "The password must contain at least one symbol: !@#$%^&*()_+")

    def get_help_text(self):  # Implementing the 'get_help_text' method
        return _(  # Returning a translated string using the 'gettext' function
            "Your password must contain at least one symbol: !@#$%^&*()_+"
        )


# Defining a subclass called 'NumericValidator' that inherits from 'BaseValidator'
class NumericValidator(BaseValidator):
    def validate(self, password, user=None):  # Implementing the 'validate' method
        # Checking if the password contains at least one digit using a regular expression
        if not re.search(r'\d', password):
            raise ValidationError(  # Raising a 'ValidationError' with a message if the condition is not met
                "The password must contain at least one number.")

    def get_help_text(self):  # Implementing the 'get_help_text' method
        return _(  # Returning a translated string using the 'gettext' function
            "Your password must contain at least one number."
        )


# Defining a subclass called 'MinimumLengthValidator' that inherits from 'BaseValidator'
class MinimumLengthValidator(BaseValidator):
    # Defining an initializer method that takes 'min_length' as a parameter
    def __init__(self, min_length=8):
        # Assigning the 'min_length' parameter to the 'min_length' attribute
        self.min_length = min_length

    def validate(self, password, user=None):  # Implementing the 'validate' method
        # Checking if the password length is less than the minimum length
        if len(password) < self.min_length:
            raise ValidationError(  # Raising a 'ValidationError' with a message if the condition is not met
                "The password must be at least %(min_length)d characters long."
                % {"min_length": self.min_length}
            )

    def get_help_text(self):  # Implementing the 'get_help_text' method
        return _(  # Returning a translated string using the 'gettext' function
            "Your password must contain at least %(min_length)d characters."
            % {"min_length": self.min_length}
        )


# Defining a subclass called 'CommonPasswordValidator' that inherits from 'BaseValidator'
class CommonPasswordValidator(BaseValidator):
    def validate(self, password, user=None):  # Implementing the 'validate' method
        common_passwords = ["password", "123456", "12345678", "1234", "qwerty", "12345", "dragon", "111111", "baseball", "football", "asdfghjkl", "123abc", "monkey", "letmein", "696969", "shadow", "master", "666666",
                            "qwertyuiop", "123321", "mustang", "1234567890", "michael", "654321", "superman", "1qaz2wsx", "7777777", "121212", "000000", "qazwsx", "123qwe", "000000", "iloveyou", "password123", "password1", "1qaz2wsx", "1q2w3e4r"]
        # Checking if the lowercase version of the password is in the list of common passwords
        if password.lower() in common_passwords:
            # Raising a 'ValidationError' with a message if the condition is met
            raise ValidationError("The password is too common.")

    def get_help_text(self):  # Implementing the 'get_help_text' method
        return _(  # Returning a translated string using the 'gettext' function
            "Your password can't be a commonly used password."
        )
