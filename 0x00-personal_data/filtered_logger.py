#!/usr/bin/python3
"""implements a log filter that will obfuscate PII fields"""
from mysql.connector import connection
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


def get_db() -> connection.MySQLConnection:
    """securely connect to the db using environment variables"""
    db_user = os.environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    db_pass = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.environ.get("PERSONAL_DATA_DB_NAME")
    db_connector = connection.MySQLConnection(
        user=db_user,
        password=db_pass,
        host=db_host,
        database=db_name)
    return db_connector


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
    cur = db_connector.cursor()
    q_users = ('SELECT * FROM users;')

    cur.execute(q_users)
    users = cur.fetchall()
    logger = get_logger()

    for usr in users:
        str = 'name={}; email={}; phone={}; ssn={}; password={}; ip={}; '\
            'last_login={}; user_agent={};'
        str = str.format(
            usr[0], usr[1], usr[2], usr[3], usr[4], usr[5], usr[6], usr[7])
        logger.info(str)

    cur.close()
    db_connector.close()


if __name__ == "__main__":
    main()
