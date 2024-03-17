from django.urls import path
from .views import MainView, SearchFormView, ErrorMessageView, SuccessView, InDatabaseView

urlpatterns = [
    path('main/', MainView.as_view(), name='main'),
    path('error-message/', ErrorMessageView.as_view(), name = 'error_message'),
    path('search-form/', SearchFormView.as_view(), name = 'search_form' ),
    path('game-present/', InDatabaseView.as_view(), name = 'game_present'),
    path('success/', SuccessView.as_view(), name = 'success')
]