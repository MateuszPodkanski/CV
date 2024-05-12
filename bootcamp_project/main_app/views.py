from django.shortcuts import render
from django.views import View
import os
from .api_handler.my_api_handler import GamesApiHandler
from .models import Game
from .forms import GameForm, FilterForm
from django.shortcuts import redirect


class MainView(View):

    template_name = 'main_app/main.html'

    def get(self, request):

        games = Game.objects.all()

        context = {
                'games': games,
        }
        return render(request,self.template_name, context)
    
    def post(self, request):
        form = FilterForm(request.POST)
        if form.is_valid():
            search_term = form.cleaned_data['search_term']
            column_parameter = form.cleaned_data['column_parameter']

            if search_term and column_parameter:
                if column_parameter == 'name':
                    games = Game.objects.filter(name__icontains=search_term)
                elif column_parameter == 'release_date':
                    games = Game.objects.filter(release_date__icontains=search_term)
                elif column_parameter == 'rating':
                    games = Game.objects.filter(rating__icontains=search_term)
                else:
                    games = Game.objects.all

            context = {'games':games}
            return render(request, self.template_name, context)
        return redirect ('main')

class BaseTemplateView(View):

    template_name = ''

    def render_template (self,request,context=None):
        return render(request, self.template_name, context or {})
    

class InDatabaseView(BaseTemplateView):
    template_name = 'main_app/game_in_database.html'

    def show_message(self ,request ,message):
        return self.render_template(request, {'message': message})   
    
    def get(self, request, message):
        return self.show_message(request,message)
    
    def post (self, request, message):
        return self.show_message(request,message)

class ErrorMessageView(BaseTemplateView):
    template_name = 'main_app/error_template.html'

    def show_error(self, request, error_message="An error occurred"):
        return self.render_template(request, {'error_message': error_message})
    
    def get (self, request, error_message=None):
        return self.show_error(request, error_message)
    
    def post(self, request, error_message=None):
        return self.show_error(request, error_message)
        
class SuccessView(BaseTemplateView):
    template_name = 'main_app/success_template.html'

    def show_success(self, request, success_message="Success"):
        return self.render_template(request, {'success_message': success_message})
    
    def get (self, request, success_message=None):
        return self.show_success(request, success_message)
    
    def post(self, request, success_message=None):
        return self.show_success(request, success_message)

    

class SearchFormView(View):
    template_name = 'main_app/search_form.html'

    def get(self, request):
        form = GameForm()
        return render(request, self.template_name, {'form':form})
        
    def post(self,request):
        form = GameForm(request.POST)

        if form.is_valid():
            game_name_form = form.cleaned_data['game_name']
            api_key = os.environ.get("RAWG_API_KEY")
            base_url = f'https://api.rawg.io/api/games?key={api_key}&search='
            games_api_handler = GamesApiHandler(slug=None, name=None, release_date = None, rating = None, base_url = base_url)
            query_params = {'search':game_name_form}
            data = games_api_handler.get_data(endpoint='', query_params=query_params)
            
            if data:
                games_api_handler.process_data(data)
                game_name = games_api_handler.get_name

                if game_name == game_name_form:
                    game_rating = games_api_handler.get_rating
                    game_release_date = games_api_handler.get_release_date

                    existing_game = Game.objects.filter(name=game_name).first()

                    if existing_game is not None:
                        print(f"Game already in database: {existing_game.name}")
                        return InDatabaseView.as_view()(request, message =  "Game is already in database")
                    else:
                        game_instance = Game.objects.create(
                        name=game_name,
                        release_date=game_release_date,
                        rating=game_rating,
                        )
                        print(f"New Game added to the database: {game_instance.name}")
                
                        games_api_handler.update_data(slug=None, name=None, release_date=None, rating=None)
                  
                        return SuccessView.as_view()(request, success_message = "Game was added!")
                else: 
                     return ErrorMessageView.as_view()(request, error_message = "There is no game like that try another one")
            
            else: 
                return ErrorMessageView.as_view()(request, error_message = "Api broke down sorry")
        
        else: 
            return ErrorMessageView.as_view()(request, error_message = "Something went wrong when validating the data, please try again")
        