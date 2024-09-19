import time
import pytest
import subprocess
import mysql.connector
from mysql.connector import Error
import docker

@pytest.fixture(scope="module", autouse=True)
def start_docker_compose(pytestconfig):

    docker_compose_file = pytestconfig.getoption("docker_compose_ecommerce")
    client = docker.from_env()

    if docker_compose_file:
        print(f"Starting Docker Compose with {docker_compose_file}")
        subprocess.run(["docker-compose", "-f", docker_compose_file, "up", "-d"], check=True)

        yield  #yield to test
    
        containers = client.containers.list()   #teardown all containers
        for container in containers:
            container.stop()
            container.remove()

    
@pytest.fixture(scope="module")
def database_connection():
    # Wait for MySQL to be ready (increase if needed)
    for i in range(15):  # Try for 10 seconds
        try:
            connection = mysql.connector.connect(user='root', password='',
                                          host='localhost',  
                                          database='ecommerce')
            
            yield connection #let other functions use the connection before closing

            connection.close()
            print("Database is ready")
            break
        except Error as e:
            print(f"Waiting for database... {e}")
            time.sleep(2)
    else:
        pytest.fail("Database didn't become ready in time")

@pytest.fixture(scope="function")
def db_cursor(database_connection):
    cursor = database_connection.cursor(buffered=True)
    yield cursor
    cursor.close()

def test_database_table_exists(db_cursor):
    # db_cursor is injected here too
    db_cursor.execute("SHOW TABLES LIKE 'users'")
    result = db_cursor.fetchone()
    assert result is not None, "Users table does not exist"

def test_database_values_exist(db_cursor):
    # db_cursor is injected here too
    db_cursor.execute("SELECT * FROM users")
    result = db_cursor.fetchone()
    assert result is not None, "No data in table"


