import pytest

from app.utils.template_manager import TemplateManager

class TestTemplateMngr():
    @pytest.fixture
    def manager(self):
        manager = TemplateManager()
        return manager
    
    def test_render_template(self, manager): 
        content:str = manager.render_template('email_verification', name='John Doe', verification_url='http://example.com/verify/1234')
        assert isinstance(content, str) == True
    
