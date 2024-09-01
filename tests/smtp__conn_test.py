import pytest
import os
import sys

# Get the directory of the current script (test file)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory (project root)
project_root = os.path.dirname(current_dir)

# Add the project root to the Python path
sys.path.append(project_root)