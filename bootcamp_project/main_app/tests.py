from django.test import TestCase,SimpleTestCase
from .models import Game
from datetime import date
from .forms import GameForm, FilterForm
from django.urls import reverse, resolve
from .views import MainView, SearchFormView, ErrorMessageView, SuccessView, InDatabaseView


class GameModelTestCase(TestCase):
    def test_game_creation(self):
        game = Game.objects.create(name="Test Game", release_date="2022-01-01",rating=4.5)

        saved_game = Game.objects.get(name="Test Game")

        self.assertEqual(saved_game.name,"Test Game")
        self.assertEqual(saved_game.release_date, date(2022,1,1))
        self.assertEqual(saved_game.rating,4.5)    

class GameFortTest(TestCase):
    def test_game_from_valid_data(self):
        form = GameForm(data={'game_name': "Test Game"})
        self.assertTrue(form.is_valid())

    def test_game_form_no_data(self):
        form = GameForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['game_name'], ['This field is required.'])

class FilterFormTest(TestCase):
    def test_filter_form_valid_data(self):
        form = FilterForm(data={'search_term': 'Test', 'column_parameter': 'name'})
        self.assertTrue(form.is_valid())
    
    def test_filter_form_invalid_data(self):
        form = FilterForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['search_term'], ['This field is required.'])
        self.assertEqual(form.errors['column_parameter'], ['This field is required.'])

class TestUrls(SimpleTestCase):
    def test_main_url_resolves(self):
        url = reverse('main')
        self.assertEqual(resolve(url).func.view_class, MainView)

    def test_error_message_url_resolves(self):
        url = reverse('error_message')
        self.assertEqual(resolve(url).func.view_class, ErrorMessageView)

    def test_search_form_url_resolves(self):
        url = reverse('search_form')
        self.assertEqual(resolve(url).func.view_class, SearchFormView)
    
    def test_game_present_url_resolves(self):
        url = reverse('game_present')
        self.assertEqual(resolve(url).func.view_class, InDatabaseView)

    def test_success_url_resolves(self):
        url = reverse('success')
        self.assertEqual(resolve(url).func.view_class, SuccessView)

