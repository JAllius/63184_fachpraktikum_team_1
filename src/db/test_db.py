import mysql.connector
import pytest
import logging

logger = logging.getLogger(__name__)

DB_HOST = "localhost"
DB_ROOT = "root"
DB_ROOT_PW = "safe123"
DB_PYTEST_NAME = "pytest"
DB_PYTEST_USER = "pytest"
DB_PYTEST_PW = "pytest"


@pytest.fixture(scope="session")
def root():
    logger.info("Connecting to mysql as root")
    mydb = mysql.connector.connect(
        host=DB_HOST,
        user=DB_ROOT,
        password=DB_ROOT_PW
    )
    yield mydb
    logger.info("Closing root session to mysql")
    mydb.disconnect()

@pytest.fixture(scope="session", autouse=True)
def init_pytest_db(root):
    cursor = root.cursor()
    cursor.execute(f"DROP DATABASE IF EXISTS {DB_PYTEST_NAME}")
    cursor.execute(f"CREATE DATABASE {DB_PYTEST_NAME}")

    cursor.execute(f"DROP USER IF EXISTS {DB_PYTEST_USER}@{DB_HOST}")
    cursor.execute(f"CREATE USER IF NOT EXISTS {DB_PYTEST_USER}@{DB_HOST} IDENTIFIED BY '{DB_PYTEST_PW}';")
    cursor.execute(f"GRANT ALL PRIVILEGES ON {DB_PYTEST_NAME}.* TO {DB_PYTEST_USER}@{DB_HOST};")

@pytest.fixture()
def db_session(init_pytest_db):
    logger.info(f"Connecting to db '{DB_PYTEST_NAME}' as user '{DB_ROOT}'")
    mydb = mysql.connector.connect(
        host=DB_HOST,
        user=DB_ROOT,
        password=DB_ROOT_PW,
        # database=DB_PYTEST_NAME
    )
    yield mydb
    logger.info(f"Closing user '{DB_ROOT}' session to db '{DB_PYTEST_USER}'")
    mydb.disconnect()

def test_root_db_access(root):
    return

def test_pytest_db(db_session):
    return

