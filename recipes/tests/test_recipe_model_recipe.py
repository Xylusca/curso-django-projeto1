from django.core.exceptions import ValidationError
from parameterized import parameterized

from recipes.models import Recipe

from .test_recipe_base import RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_no_default(self):
        recipe = Recipe(
            category=self.make_category(name='Test Default Category'),
            author=self.make_author(username='newuser'),
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug-for-no-defaults',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            preparation_steps='Recipe Preparation Steps',
        )
        recipe.full_clean()
        recipe.save()
        return recipe

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

    def test_recipe_preparation_step_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_default()
        self.assertFalse(
            recipe.preparation_steps_is_html,
            msg='Recipe preparation_steps_is_html is not False',
        )

    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_default()
        self.assertFalse(
            recipe.is_published,
            msg='Recipe is_published is not False',
        )

    def test_recipe_string_representation(self):
        needed = 'TESTING REPRESENTATION'
        self.recipe.title = needed
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(
            str(self.recipe), 'TESTING REPRESENTATION',
            msg=f'Recipe string representation must be '
            f'"{needed}" but "{str(self.recipe)}" was received.'
        )
