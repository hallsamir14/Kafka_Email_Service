import pytest

from app.emailer import emailer
from app.utils.template_manager import TemplateManager


class TestEmail:
    @pytest.fixture
    def manager(self):
        manager = TemplateManager()  # initialize template manager to use in email test
        return manager

    def test_email(self, manager):

        content: str = manager.render_template(
            "email_verification",
            name="John Doe",
            verification_url="http://example.com/verify/1234",
        )  # test send a email
        emailer.send_email("content", content, "recipient")
