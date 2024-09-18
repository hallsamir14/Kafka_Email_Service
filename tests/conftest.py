import pytest
from typing import Optional
import mysql.connector
from mysql.connector import errorcode


def pytest_addoption(parser):
    parser.addoption("--docker-compose", action="store", default=None, help="test-docker-compose.yml")

@pytest.fixture(scope="session") #tear down fixture once for the whole file
def docker_compose_file(pytestconfig):
    return pytestconfig.rootdir / "test" / "test-docker-compose.yml"

@pytest.fixture(scope = "session")
def db_connection():
    conn = None
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ecommerce"
        )
        yield conn
    except mysql.connector.Error as e:
        pytest.fail(f"Failed to connect to MySQL: {e}")
    finally:
        if conn.is_connected():
            conn.close()

@pytest.fixture(scope="function")
def db_cursor(db_connection):
    cursor = db_connection.cursor(dictionary=True)
    yield cursor
    cursor.close()