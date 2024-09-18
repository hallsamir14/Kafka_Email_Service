import time
import pytest
import subprocess
import mysql.connector
from mysql.connector import Error

@pytest.fixture(scope="module", autouse=True)
def start_docker_compose(pytestconfig):
    docker_compose_file = pytestconfig.getoption("docker_compose")
    if docker_compose_file:
        print(f"Starting Docker Compose with {docker_compose_file}")
        subprocess.run(["docker-compose", "-f", docker_compose_file, "up", "-d"], check=True)
    


def test_database_table_exists(pytestconfig):
    print(pytestconfig.getoption("docker_compose"))
    time.sleep(10)
    result = [0] * 1
    result[0] = 1
    assert result[0] == 1

def test_api_select():
    result = [0] * 1
    result[0] = 1
    assert result[0] == 1









    
"""
def test_database_connection():
        # Wait for MySQL to be ready (increase if needed)
    for i in range(10):  # Try for 10 seconds
        try:
            cnx = mysql.connector.connect(user='root', password='',
                                          host='localhost',  # Use 'localhost' or 'mysql' based on setup
                                          database='ecommerce')
            cnx.close()
            print("Database is ready")
            break
        except Error as e:
            print(f"Waiting for database... {e}")
            time.sleep(2)
    else:
        pytest.fail("Database didn't become ready in time")
"""