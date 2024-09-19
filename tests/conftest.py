import pytest
import os


def pytest_addoption(parser):
    conftest_dir = os.path.dirname(os.path.abspath(__file__))

    # Navigate to the parent directory, then into the 'tests' folder
    ecommerce_docker_compose_file = os.path.join(conftest_dir,'integration_tests', 'test-docker-compose-ecommerce.yml')
    parser.addoption("--docker-compose-ecommerce", action="store", default=ecommerce_docker_compose_file, help="test-docker-compose-ecommerce.yml")


