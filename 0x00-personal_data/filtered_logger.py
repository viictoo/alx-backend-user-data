#!/usr/bin/env python3
"""implements a log filter that will obfuscate PII fields"""
from mysql.connector.connection import MySQLConnection
import os
import re
from typing import List
import logging

PII_FIELDS = ('name', 'email', 'phone', 'password', 'ssn')


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str,
) -> str:
    """returns obfuscated logs using re
    Args:
        fields:     a list of strings representing all fields to obfuscate
        redaction:  a string representing by what the field will be obfuscated
        message:    a string representing the log line
        separator:  a string representing by which character is
                    separating all fields in the log line
    """
    logtext = message
    for field in fields:
        logtext = re.sub(field + "=.*?" + separator,
                         field + "=" + redaction + separator, logtext)
    return logtext


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
