from django.urls import reverse, resolve
from recipes import views

from unittest.mock import patch
from .test_recipe_base import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):

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

    def test_recipe_category_template_dont_load_recipe_not_published(self):
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))

        # Check if the recipe has been published or not
        response = self.client.get(
            reverse('recipes:category', kwargs={
                    'category_id': recipe.category.id})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_is_paginated(self):
        category_test = self.make_category()
        for i in range(8):
            kwargs = {'slug': f'r{i}',
                      'author_data': {'username': f'u{i}'},
                      }
            self.make_recipe_with_category_being_same(
                category_data=category_test, **kwargs)

        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(
                reverse('recipes:category',
                        kwargs={'category_id': 1}))
            recipes = response.context['recipes']
            paginator = recipes.paginator

        self.assertEqual(paginator.num_pages, 3)
        self.assertEqual(len(paginator.get_page(1)), 3)
        self.assertEqual(len(paginator.get_page(2)), 3)
        self.assertEqual(len(paginator.get_page(3)), 2)
