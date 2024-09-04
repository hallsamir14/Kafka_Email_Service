import pytest
import os
import sys

# Get the directory of the current script (test file)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory (project root)
project_root = os.path.dirname(current_dir)

# Add the project root to the Python path
sys.path.append(project_root)

from app.utils.template_manager import TemplateManager

class TestTemplateMngr():
    @pytest.fixture
    def manager(self):
        manager = TemplateManager()
        return manager
    
    def test_render_template(self, manager): 
        content:str = manager.render_template('email_verification', name='John Doe', verification_url='http://example.com/verify/1234')
        assert isinstance(content, str) == True
    
