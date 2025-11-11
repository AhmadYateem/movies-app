from django.forms import ModelForm
from .models import Video
from django import forms


class VideoForm(ModelForm):
	class Meta:
		model = Video
		fields = ['MovieTitle', 'Actor1Name', 'Actor2Name', 'DirectorName', 'MovieGenre', 'ReleaseYear']
		widgets = {
			'MovieTitle': forms.TextInput(attrs={'placeholder': 'Enter movie title'}),
			'Actor1Name': forms.TextInput(attrs={'placeholder': 'Enter actor name'}),
			'Actor2Name': forms.TextInput(attrs={'placeholder': 'Enter actor name'}),
			'DirectorName': forms.TextInput(attrs={'placeholder': 'Enter director name'}),
			'MovieGenre': forms.TextInput(attrs={'placeholder': 'Enter genre'}),
			'ReleaseYear': forms.NumberInput(attrs={'placeholder': 'Enter year'}),
		}
		labels = {
			'MovieTitle': 'Movie Title',
			'Actor1Name': 'Actor 1 Name',
			'Actor2Name': 'Actor 2 Name',
			'DirectorName': 'Director Name',
			'MovieGenre': 'Movie Genre',
			'ReleaseYear': 'Release Year',
		}