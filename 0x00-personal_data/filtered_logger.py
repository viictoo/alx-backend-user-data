#!/usr/bin/env python3
"""implements a log filter that will obfuscate PII fields"""
from mysql.connector.connection import MySQLConnection
import os
import re
from typing import List
import logging

PII_FIELDS = ('name', 'email', 'phone', 'password', 'ssn')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    This function returns the log message obfuscated.
    >>> filter_datum = __import__('filtered_logger').filter_datum
    >>> fields = ["password", "date_of_birth"]
    >>> messages = ["name=egg;email=eggmin@eggsample.com;password=eggcellent;
    date_of_birth=12/12/1986;",
    "name=bob;email=bob@dylan.com;password=bobbycool;date_of_birth=03/04/1993;"]
    >>> for message in messages:
    ...    print(filter_datum(fields, 'xxx', message, ';'))
    ...
    name=egg;email=eggmin@eggsample.com;password=xxx;date_of_birth=xxx;
    name=bob;email=bob@dylan.com;password=xxx;date_of_birth=xxx;
    >>>
    """
    for field in fields:
        message = re.sub(
            rf'{field}=([^{separator}]+)', f'{field}={redaction}', message)
    return message


def get_logger() -> logging.Logger:
    """return logging.Logger object"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    # use PII fields to redact personal info
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> MySQLConnection:
    """securely connect to the db using environment variables"""
    return MySQLConnection(
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        port=3306,
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        database=os.getenv("PERSONAL_DATA_DB_NAME")
    )


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ filter values in incoming log records using filter_datum.
            Values for fields in fields should be filtered
        """
        return filter_datum(
            self.fields, self.REDACTION, super(
                RedactingFormatter, self).format(record), self.SEPARATOR)


def main() -> None:
    """ main function that takes no arguments and returns nothing
        obtain a database connection using get_db and retrieve all
        rows in users table and disp each row under filtered format
    """

    db_connector = get_db()
    csr = db_connector.cursor()
    csr.execute("SELECT * FROM users;")
    logger = get_logger()
    for row in csr:
        message = ""
        for i in range(len(row)):
            message += f"{csr.column_names[i]}={str(row[i])}; "
        logger.info(message)
    csr.close()
    db_connector.close()


if __name__ == "__main__":
    main()
