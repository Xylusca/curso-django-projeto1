from django.test import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand(
        [
            ("username", "Your username"),
            ("email", "Your e-mail"),
            ("first_name", "Ex.: Lucas"),
            ("last_name", "Ex.: Pereira"),
            ("password", "Type your password"),
            ("password2", "Repeat your password"),
        ]
    )
    def test_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs["placeholder"]
        self.assertEqual(current_placeholder, placeholder)