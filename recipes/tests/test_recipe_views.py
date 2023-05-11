from django.urls import reverse, resolve
from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipesViewsTest(RecipeTestBase):
    def test_recipes_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_tamplete(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_tamplate_shows_no_recipes_found_is_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            '<h1 class="fa-3x">NOT FOUND</h1>',
            response.content.decode('utf-8'),
        )

    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe(author_data={
            'first_name': 'lucas'
        })
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        self.assertIn('lucas', content)

    def test_recipes_category_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_400_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        need_title = 'This is a category test'
        self.make_recipe(title=need_title)

        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1}))
        content = response.content.decode('utf-8')

        self.assertIn(need_title, content)

    def test_recipes_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returns_400_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_the_correct_recipe(self):
        need_title = 'This is a detail page - It load one recipe'
        self.make_recipe(title=need_title)

        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1}))
        content = response.content.decode('utf-8')

        self.assertIn(need_title, content)
