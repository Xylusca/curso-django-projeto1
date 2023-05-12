from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_recipe_base import RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def test_recipe_title_raises_error_if_title_has_more_than_65_chars(self):
        self.recipe.title = "A" * 66

        with self.assertRaisesMessage(ValidationError, 'Certifique-se de que o valor tenha no máximo 65'):
            self.recipe.full_clean()

    @parameterized.expand([
        ('title', 66,
         'Certifique-se de que o valor tenha no máximo 65 caracteres'),
        ('description', 165,
         'Certifique-se de que o valor tenha no máximo 165 caracteres'),
        ('preparation_time_unit', 65,
         'Certifique-se de que o valor tenha no máximo 65 caracteres'),
        ('servings_unit', 65,
         'Certifique-se de que o valor tenha no máximo 65 caracteres'),
    ])
    def test_recipe_fields_max_length(self, field, max_length, error_message):
        setattr(self.recipe, field, 'A' * (max_length+1))
        with self.assertRaisesMessage(ValidationError, error_message):
            self.recipe.full_clean()
