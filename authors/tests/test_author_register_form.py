from django.test import TestCase
from django.urls import reverse
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
    def test_fields_placeholder(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs["placeholder"]
        self.assertEqual(current_placeholder, placeholder)

    @parameterized.expand(
        [
            (
                "username",
                (
                    "Obrigatório. 150 caracteres ou menos. "
                    "Letras, números e @/./+/-/_ apenas."
                ),
            ),
            (
                "password",
                (
                    "Password must have at least one uppercase letter, "
                    "one lowercase letter and one number. The length should be"
                    " at least 8 characters."
                ),
            ),
        ]
    )
    def test_fields_help_text(self, fields, needed):
        form = RegisterForm()
        current = form[fields].field.help_text
        self.assertEqual(current, needed)


class AuthorRegisterFormIntegrationTest(TestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            "username": "user",
            "first_name": "first",
            "last_name": "last",
            "email": "email@anyemail.com",
            "password": "Str0ngP@ssword1",
            "password2": "Str0ngP@ssword1",
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand(
        [
            ("username", "Este campo é obrigatório."),
            ("first_name", "Write your first name"),
            ("last_name", "Write your last name"),
            ("password", "Password must not be empty"),
            ("password2", "Este campo é obrigatório."),
            ("email", "E-mail is required"),
        ]
    )
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ""
        url = reverse("authors:create")
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode("utf-8"))
        self.assertIn(msg, response.context["form"].errors.get(field))
