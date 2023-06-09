from django.urls import reverse, resolve
from recipes import views

from unittest.mock import patch
from .test_recipe_base import RecipeTestBase


class RecipeSearchViewTest(RecipeTestBase):
    def test_recipe_search_uses_correct_view_function(self):
        url = reverse('recipes:search')
        resolved = resolve(url)
        self.assertIs(resolved.func, views.search)

    def test_recipe_search_loads_correct_view_tamplete(self):
        response = self.client.get(reverse('recipes:search') + '?q=teste')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        url = reverse('recipes:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse('recipes:search') + '?q=test'
        response = self.client.get(url)
        self.assertIn(
            'Search for &quot;test&quot;',
            response.content.decode('utf-8')
        )

    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = 'this is recipe one'
        title2 = 'this is recipe two'

        recipe1 = self.make_recipe(
            title=title1, slug='one', author_data={'username': 'one'}
        )
        recipe2 = self.make_recipe(
            title=title2, slug='two', author_data={'username': 'two'}
        )

        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{search_url}?q={title1}')
        response_both = self.client.get(f'{search_url}?q=this')

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])

    def test_recipe_search_can_find_recipe_by_description(self):
        description1 = 'description one'
        description2 = 'description two'

        recipe1 = self.make_recipe(
            description=description1, slug='one', author_data={'username': '1'}
        )
        recipe2 = self.make_recipe(
            description=description2, slug='two', author_data={'username': '2'}
        )

        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{search_url}?q={description1}')
        response_both = self.client.get(f'{search_url}?q=description')

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])

    def test_recipe_search_is_paginated(self):
        for i in range(8):
            kwargs = {'slug': f'r{i}',
                      'author_data': {'username': f'u{i}'},
                      }
            self.make_recipe(**kwargs)

        with patch('recipes.views.PER_PAGE', new=3):
            search_url = reverse('recipes:search')
            response = self.client.get(f'{search_url}?q=r')
            recipes = response.context['recipes']
            paginator = recipes.paginator

        self.assertEqual(paginator.num_pages, 3)
        self.assertEqual(len(paginator.get_page(1)), 3)
        self.assertEqual(len(paginator.get_page(2)), 3)
        self.assertEqual(len(paginator.get_page(3)), 2)
