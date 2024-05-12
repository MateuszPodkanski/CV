from django.test import TestCase,SimpleTestCase,RequestFactory,Client
from .models import Game
from datetime import date
from .forms import GameForm, FilterForm
from django.urls import reverse, resolve
from .views import MainView, SearchFormView, ErrorMessageView, SuccessView, InDatabaseView
from django.contrib.auth.models import User
from unittest.mock import patch, Mock
from main_app.api_handler.my_api_handler import GamesApiHandler, MyApiHandler

class MyApiHandlerTestCase(TestCase):
    def setUp(self):
        self.base_url = 'http://example.com'
        self.api_handler = MyApiHandler(self.base_url)


    @patch('myapp.api_handlers.requests.get')
    def test_get_data_success(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {'data': 'mocked_data'}

        data = self.api_handler.get_data('/endpoint')

        self.assertIsNotNone(data)
        self.assertEqual(data, {'data': 'mocked_data'})

    @patch('myapp.api_handlers.requests.get')
    def test_get_data_failure(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 404

        data = self.api_handler.get_data('/invalid_endpoint')

        self.assertIsNone(data)

class GamesApiHandler(TestCase):

    def setUp(self):
        self.games_api_handler = GamesApiHandler(slug='example_slug',name='example_name',release_date='01-01-2012',rating='4.5')

    def test_update_data(self):
        self.games_api_handler.update_data(slug='new_slug', name='new_name', release_date ='new_release_date', rating='new_release_date') 

        self.assertEqual(self.games_api_handler.get_slug,'new_slug') 
        self.assertEqual(self.games_api_handler.get_name,'new_name')     
        self.assertEqual(self.games_api_handler.get_name,'new_release_date')
        self.assertEqual(self.games_api_handler.get_name,'new_rating')


class GameModelTestCase(TestCase):
    def test_game_creation(self):
        game = Game.objects.create(name="Test Game", release_date="2022-01-01",rating=4.5)

        saved_game = Game.objects.get(name="Test Game")

        self.assertEqual(saved_game.name,"Test Game")
        self.assertEqual(saved_game.release_date, date(2022,1,1))
        self.assertEqual(saved_game.rating,4.5)    

class GameFormTest(TestCase):
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
        self.client = Client()
        self.user = User.objects.create(username='test_user')
        self.game1 = Game.objects.create(name='Game 1', release_date='2022-01-01', rating=4.5)
        self.game2 = Game.objects.create(name='Game 2', release_date='2022-02-01', rating=3.8)

    
    def test_main_view_get(self):
        response = self.client.get(reverse('main'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'main_app/main.html')

        self.assertIn('games', response.context)

        games = response.context['games']
        self.assertEqual(len(games),2)
        self.assertIn(self.game1,games)
        self.assertIn(self.game2,games)


    def test_main_view_post_valid_form(self):
        data = {'search_term': 'Game 1', 'column_parameter':'name'}
        response = self.client.get(reverse('main'),data)

        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'main_app/main.html')
        self.assertIn('games',response.context)
        
        games = response.context['games']
        self.assertEqual(len(games),1)
        self.assertIn(self.game1, games)


    def test_main_view_post_invalid_form(self):

        data = {}

        response = self.client.get(reverse('main'),data)
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

class InDatabaseViewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.message = "Test game in database message"

    def test_indatabase_view(self):

        request = self.factory.get(reverse('message'))

        response = InDatabaseView.as_view()(request)

        self.assertEqual(response.status_code,200)

        self.assertTemplateUsed(response,'main_app/game_in_database.html')

        self.assertIn('message',response)

        self.assertEqual(response.context['message'],self.message)

class SearchFormViewTestCase(TestCase):
    
    def setUp(self):
        self.factory = RequestFactory()

    def test_search_form_get(self):
        request = self.factory.get(reverse('search_form'))
        response = SearchFormView.as_view()(request)

        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'main_app/search_form.html')
        self.assertIn('form',response.context)
        self.assertIsInstance(response.context['form'], GameForm)

    @patch('main_app.views.Game.objects.filter')
    @patch('main_app.views.GamesApiHandler')
    def test_search_form_post(self, mock_handler, mock_filter):
        mock_handler_instance = mock_handler.return_value
        mock_handler_instance.get_name.return_value = 'Test Game'
        mock_handler_instance.get_rating.return_value = 8.5
        mock_handler_instance.get_release_date.return_value = "2022-01-01"

        mock_filter.return_value.first.return_value = None

        request = self.factory.post(reverse('search_form'), data={'game_name': 'Test Game'})
        response = SearchFormView.as_view()(request)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('success'))

    @patch('main_app.views.GamesApiHandler')
    def test_api_data_fetching(self, mock_handler):
        
        request = self.factory.post(reverse('search_form'), data={'game_name': 'Test Game'})

        mock_handler_instance = mock_handler.return_value
        mock_handler_instance.get_data_return_value = {'game_name': 'Test Game', 'rating': 8.5, 'release_date': '2022-01-01'}

        response = SearchFormView.as_view()(request)

        self.assertEqual(response.status_code, 200)

        self.assertIn('game_name', response.context)
        self.assertEqual(response.context['game_name'], 'Test Game')
        self.assertIn('rating', response.context)
        self.assertEqual(response.context['rating'], 8.5)
        self.assertIn('release_date',response.context)
        self.assertEqual(response.context['release_date'], '2022-01-01')

    @patch('main_app.views.GapesApiHandler')
    def test_api_data_processing(self, mock_handler):
        request = self.factory.post(reverse('seach_form'), data={'game_name': 'Test Game'})
        
        mock_handler_instance = mock_handler.return_value
        mock_handler_instance.get_data.return_value = {'game_name': 'Test Game', 'rating': 8.5, 'release_date': '2022-01-01'}

        response = SearchFormView.as_view()(request)

        game = Game.objects.filter(name = 'Test Game').first()

        self.assertIsNotNone(game)
        self.assertEqual(game.rating, 8.5)
        self.assertEqual(game.release_date, '2022-01-01')

        self.assertEqual(response.status.code, 302)
        self.assertRedirects (response,reverse('success'))

    
    def test_existing_game_handling(self):
        existing_game = Game.objects.create(name='Test game',release_date ='2020-01-01', rating=5.0)

        request = self.factory.post(reverse('search_form'), data={'game_name': 'Test Game'})

        response = SearchFormView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Game is already in database")

    @patch('main_app.views.GamesApiHandler.get_data')
    def test_api_error_handling(self, mock_get_data):
        mock_get_data.return_value = None

        request = self.factory.post(reverse('search_form'), data={'game_name': 'Test Game'})

        response = SearchFormView.as_view()(request)

        self.assertEqual(response.status_code,200)
        self.assertContains(response, "Api broke down sorry")

    def test_invalid_form_data(self):
            
        request = self.factory.post(reverse('search_form'), data={})

        response = SearchFormView.as_view()(request)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'main_app/search_form.html')

        self.assertContains(response, "")

        self.assertContains(response, "Something went wrong when validating the data, please try again")

    def test_game_not_found_error_handling(self):

        request = self.factory.post(reverse('search_form'),data={'game_name':'Non existin game'})

        response = SearchFormView.as_view(request)

        self.assertEqual(response.status_code,200)

        self.assertContains(response, "There is no game like that. Please try another one.")
