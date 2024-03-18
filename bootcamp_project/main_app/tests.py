from django.test import TestCase,SimpleTestCase,RequestFactory
from .models import Game
from datetime import date
from .forms import GameForm, FilterForm
from django.urls import reverse, resolve
from .views import MainView, SearchFormView, ErrorMessageView, SuccessView, InDatabaseView
from django.contrib.auth.models import User


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

class MainViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username='test_user')
        self.game1 = Game.objects.create(name='Game 1', release_date='2022-01-01', rating=4.5)
        self.game2 = Game.objects.create(name='Game 2', release_date='2022-02-01', rating=3.8)

    
    def test_main_view_get(self):
        request = self.factory.get(reverse('main'))

        response = MainView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'main_app/main.html')

        self.assertIn('games', response.context)

        games = response.context['games']
        self.assertEqual(len(games),2)
        self.assertIn(self.game1,games)
        self.assertIN(self.game2,games)

    
    
    def test_main_view_post_valid_form(self):
        data = {'search_term': 'Game 1', 'column_parameter':'name'}
        request = self.factory.post(reverse('main'),data)

        response = MainView.as_view()(request)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'main_app/main.html')
        self.assertIn('games',response.context)
        
        games = response.context['games']
        self.assertEqual(len(games),1)
        self.assertIn(self.game1, games)


    def test_main_view_post_invalid_form(self):

        data = {}
        request = self.factory.post(reverse('main', data))

        response = MainView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main'))


class SuccessViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.success_message = "Test success message"

    def test_success_view_get(self):
                
        request = self.factory.get(reverse('success'))

        response = SuccessView.as_view()(request)

        self.assertEqual(response.status_code,200)
     
        self.assertTemplateUsed(response,'main_app/success_template.html')
        self.assertIn('success_message',response)
        self.assertEqual(response.context['success_message'], self.success_message)

class ErrorMessageViewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.error_message = "Test error message"
    
    def test_error_message_view(self):

        request = self.factory.get(reverse('error_message'))

        response = ErrorMessageView.as_view()(request)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'main_app/error_template.html')

        self.assertIn('error_message',response)
        self.assertEqual(response.context['error_message'], self.error_message)

