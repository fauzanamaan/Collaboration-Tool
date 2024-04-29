from django.test import TestCase
from .hashers import CaesarBCryptPasswordHasher

# Create your tests here.


def test_caesar_bcrypt_password_hasher():
    hasher = CaesarBCryptPasswordHasher()

    # Test encode method
    password = "password123"
    salt = hasher.salt()
    encoded_password = hasher.encode(password, salt)
    assert encoded_password is not None

    # Test decode method
    decoded_password = hasher.decode(encoded_password)
    assert decoded_password is not None

    # Test verify method
    assert hasher.verify(password, encoded_password)

    # Test safe_summary method
    summary = hasher.safe_summary(encoded_password)
    assert summary is not None

    # Test must_update method
    assert not hasher.must_update(encoded_password)

    print("All tests passed.")


test_caesar_bcrypt_password_hasher()
