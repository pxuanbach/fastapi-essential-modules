import secrets
import string


def generate_random_string(length: int = 8) -> str:
    return "".join(secrets.choice(string.ascii_lowercase) for i in range(length))
