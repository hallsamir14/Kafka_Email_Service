import pytest
import os


def pytest_addoption(parser):
    conftest_dir = os.path.dirname(os.path.abspath(__file__))

    # Navigate to the parent directory, then into the 'tests' folder
    docker_compose_file = os.path.join(conftest_dir,'test-docker-compose.yml')
    parser.addoption("--docker-compose", action="store", default=docker_compose_file, help="test-docker-compose.yml")

