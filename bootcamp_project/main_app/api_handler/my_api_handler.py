import requests
from ..models import Game


class MyApiHandler:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_data(self, endpoint, query_params = None):
        api_url = f'{self.base_url}'
        response = requests.get(api_url, params=query_params)
        return response.json() if response.status_code == 200 else None

class GamesApiHandler(MyApiHandler):
    
    def __init__(self, slug, name, release_date, rating,base_url):
        super().__init__(base_url)
        self._slug = None
        self._name = None
        self._release_date = None
        self._rating = None

    def update_data(self, slug, name, release_date, rating):
        self.slug = slug
        self.name = name
        self.release_date = release_date
        self.rating = rating

    @property
    def get_slug(self):
        return self._slug
    
    @property
    def get_name(self):
        return self._name
    
    @property
    def get_release_date(self):
        return self._release_date

    @property
    def get_rating(self):
        return self._rating
    
    def process_data(self, data):
        if 'results' in data and data['results']:
            game_info = data['results'][0]
            self._slug = game_info.get('slug')
            self._name = game_info.get('name')
            self._release_date = game_info.get('released')
            self._rating = game_info.get('rating')

    @staticmethod
    def game_exists(game_name):
        existing_game = Game.objects.filter(name=game_name).first()

        print(existing_game)