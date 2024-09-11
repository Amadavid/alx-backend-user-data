#!/usr/bin/env python3
"""
    Module implementing logging with obfuscation

"""
import logging
import re
import os
import mysql.connector
from mysql.connector import connection
from typing import List, Tuple, Optional


PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Uses regex to obfuscate and log data"""
    pattern = f"({'|'.join(fields)})=[^{separator}]*"
    # replacement = lambda m: f"{m.group(1)}={redaction}"
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initializes FORMAT class attribute"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filters values for incoming log records"""
        msg = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Returns logging.logger object"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(list(PII_FIELDS))
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def get_db() -> Optional[connection.MySQLConnection]:
    """Connects to the database and returns the connection object"""
    db_username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_SB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    if not db_name:
        raise ValueError("The environment variable\
                         PERSONAL_DATA_DB_NAME is not set")
    try:
        conn = mysql.connector.connect(
                user=db_username,
                password=db_password,
                host=db_host,
                database=db_name
                )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def main():
    """Retrieves all rows from users table"""
    db_connect = get_db()
    cursor = database.cursor()
    query = "SELECT * FROM users;"
    cursor.execute(query)
    cols = [col[0] for col in cursor.description]
    logger = get_logger()

    for row in cursor:
        row_str = ''.join(f'{column}={value}{RedactingFormatter.SEPARATOR} '
                          for col, value in zip(cols, row))
        logger.info(row_str)

    cursor.close()
    db_connect.close()


if __name__ == "__main__":
    main()
