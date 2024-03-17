from django import forms

class GameForm(forms.Form):
    game_name = forms.CharField(label='Enter Game Name', max_length=100)

class FilterForm(forms.Form):
    search_term = forms.CharField(label='Search Term',max_length=100)
    column_parameter = forms.ChoiceField(
        label = 'Column Parameter',
        choices = [
            ('name', 'Name'),
            ('release_date', 'Year of Publishment'),
            ('rating', 'Grade')
        ]
    )