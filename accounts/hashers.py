import hashlib  # Import the hashlib module for hashing functions
import bcrypt  # Import the bcrypt module for the Bcrypt hashing algorithm
import binascii  # Import the binascii module for binary-to-text encoding/decoding
from gettext import gettext as _  # Import the gettext function for translation
# Import the constant_time_compare function from the django.utils.crypto module
from django.utils.crypto import constant_time_compare
# Import the BasePasswordHasher class from the django.contrib.auth.hashers module
from django.contrib.auth.hashers import BasePasswordHasher, mask_hash


def caesar_cipher(text, shift):
    ciphertext = ""
    for char in text:
        if char.isalpha():
            shift_amount = shift % 26
            new_char = chr(
                ((ord(char.lower()) - ord("a") + shift_amount) % 26) + ord("a"))
            if char.isupper():
                new_char = new_char.upper()
            ciphertext += new_char
        else:
            ciphertext += char
    return ciphertext


class CustomHasher():
    """
    CustomHasher class for custom hashing algorithm.
    """

    @staticmethod
    def check_even(number):
        """
        Checks if the given number  is even.
        Returns the number if it is even, otherwise returns the number plus 1.
        """
        if number % 2 == 0:
            return number  # Return the number if it is even
        else:
            return number + 1  # Return the number plus 1 if it is odd

    @staticmethod
    def sum_and_division(plaintext_password, index=0, total=0):
        """
        Calculates the sum and division of the ASCII values of the characters in the plaintext password.
        """
        if index < len(plaintext_password):
            char = plaintext_password[index]
            total += ord(char)
            total += ord(char)*2  # Multiply the ASCII value, not the character
            return CustomHasher.sum_and_division(plaintext_password, index + 1, total)
        else:
            return (CustomHasher.check_even(total) // 2) % 13

    @staticmethod
    def custom_hash(plaintext_password, index=0, hash_password=""):
        """
        Custom hash function that combines the plaintext password and a salt to generate a hash value.
        """
        prime = 131  # Define a prime number for hashing
        salt = str(CustomHasher.sum_and_division(plaintext_password))
        new_plaintext = plaintext_password + salt
        if index < (len(new_plaintext)-5):
            # Get the character at the current index
            char = new_plaintext[index]

            # Add the square of the ASCII value modulo prime to the hash_password
            # Convert the result to a string to avoid ValueError
            ascii_decimal = ((pow(ord(char), 4)) % prime)
            if ascii_decimal > 255:
                ascii_decimal -= 50
            hash_password += chr(ascii_decimal)

            # Recursively call the function for the next character
            return CustomHasher.custom_hash(plaintext_password, index + 1, hash_password)

        else:
            # Return the even hash_password divided by 2
            return hash_password

    @staticmethod
    def custom_final_hash(password, iterations):
        """
        Calculates the final hash value for the given password and salt using the custom hash algorithm.
        It concatenates the password and salt together to form the plain_text.
        """
        # Calculate the initial hash value using the CustomHash function.
        hash_password = CustomHasher.custom_hash(password)
        for i in range(iterations):
            # Add the CustomHash value to the hash_password for the specified number of iterations.
            # Hash the current hash_password, not the original password
            hash_password += CustomHasher.custom_hash(password)
        return hash_password


class CaesarBCryptPasswordHasher(BasePasswordHasher):
    """
    Secure password hashing using Caesar cipher and then the bcrypt algorithm.
    """

    algorithm = "bcrypt_caesar"
    digest = hashlib.sha256
    library = ("bcrypt", "bcrypt")
    rounds = 12

    def salt(self):
        """
        Generates a salt value for the bcrypt algorithm.
        """
        bcrypt = self._load_library()
        return bcrypt.gensalt(self.rounds)

    def encode(self, password, salt):
        """
        Encodes the password using the Caesar cipher and the custom hash algorithm,
        and then applies the bcrypt algorithm for additional security.
        """
        bcrypt = self._load_library()
        password = caesar_cipher(password, 13)  # Add a shift value
        password = CustomHasher.custom_final_hash(password, 25)
        password = password.encode()
        # Hash the password prior to using bcrypt to prevent password truncation as described in #20138.
        if self.digest is not None:
            # Use binascii.hexlify() because a hex encoded bytestring is str.
            password = binascii.hexlify(self.digest(password).digest())

        data = bcrypt.hashpw(password, salt)
        return "%s$%s" % (self.algorithm, data.decode("ascii"))

    def decode(self, encoded):
        """
        Decodes the encoded password and returns the algorithm, salt, and checksum.
        """
        algorithm, empty, algostr, work_factor, data = encoded.split("$", 4)
        assert algorithm == self.algorithm
        return {
            "algorithm": algorithm,
            "algostr": algostr,
            "checksum": data[22:],
            "salt": data[:22],
            "work_factor": int(work_factor),
        }

    def verify(self, password, encoded):
        """
        Verifies if the given password matches the encoded password.
        """
        algorithm, data = encoded.split("$", 1)
        assert algorithm == self.algorithm
        encoded_2 = self.encode(password, data.encode("ascii"))
        return constant_time_compare(encoded, encoded_2)

    def safe_summary(self, encoded):
        """
        Returns a summary of the encoded password, hiding sensitive information.
        """
        decoded = self.decode(encoded)
        return {
            _("algorithm"): decoded["algorithm"],
            _("work factor"): decoded["work_factor"],
            _("salt"): mask_hash(decoded["salt"]),
            _("checksum"): mask_hash(decoded["checksum"]),
        }

    def must_update(self, encoded):
        """
        Checks if the encoded password needs to be updated based on the work factor.
        """
        decoded = self.decode(encoded)
        return decoded["work_factor"] != self.rounds

    def harden_runtime(self, password, encoded):
        """
        Increases the computational cost of the bcrypt algorithm to harden runtime.
        """
        _, data = encoded.split("$", 1)
        salt = data[:29]  # Length of the salt in bcrypt.
        rounds = data.split("$")[2]
        # work factor is logarithmic, adding one doubles the load.
        diff = 2 ** (self.rounds - int(rounds)) - 1
        while diff > 0:
            self.encode(password, salt.encode("ascii"))
            diff -= 1
