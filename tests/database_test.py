import pytest
from app.utils import database_connection


@pytest.fixture(scope="session", autouse=True)
def start_docker_compose(pytestconfig):
    docker_compose_file = pytestconfig.getoption("docker_compose")
    if docker_compose_file:
        # Use subprocess or other method to start docker-compose
        print(f"Starting Docker Compose with {docker_compose_file}")


def test_database_connection(db_cursor):
    db_cursor.execute("SELECT 1")               #then use database connection code here
    result = db_cursor.fetchone()
    assert result[0] == 1

def test_database_table_exists(db_cursor):
    db_cursor.execute("SHOW TABLES LIKE 'users")
    result = db_cursor.fetchone()
    assert result[0] is not None, "Users table does not exist"

def test_api_select(db_cursor):
    db_cursor.execute("SELECT * FROM users")
    for row in db_cursor.fetchall():
        print(row)
