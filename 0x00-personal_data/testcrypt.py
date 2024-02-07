""" Module that hashes password using bcrypt
    and logs some formatted info to a file
"""
import logging
import bcrypt
"""
Logging Levels
    DEBUG
    INFO
    WARNING
    ERROR
    CRITICAL
"""

logging.basicConfig(
    filename="bcrypt.log",
    level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(levelno)s:%(message)s'
)

MAX_TRIES = 5


def check_password():
    password = b"super secret password"

    salt = bcrypt.gensalt()
    logging.debug(f"salt generated {salt}")

    hashed = bcrypt.hashpw(password, bcrypt.gensalt(prefix=b"2a"))
    # kdf = bcrypt.kdf(
    #     password=password,
    #     salt=salt,
    #     desired_key_bytes=32,
    #     rounds=100)

    logging.warning(hashed)

    for _ in range(MAX_TRIES):
        input_password = input("Enter your password: ")

        if bcrypt.checkpw(input_password.encode(), hashed):
            print("Password is correct. Access granted.")
            logging.info("login: success")
            return True

        print("Password is incorrect. Please try again.")

    print("Exceeded maximum number of tries. Access denied.")
    logging.warning("login: maximum retries exceeded")
    return False


check_password()
