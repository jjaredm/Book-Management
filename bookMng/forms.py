from django import forms
from django.forms import ModelForm
from .models import Book


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = [
            'name',
            'web',
            'price',
            'genre',
            'picture',
        ]

class BookSearchForm(forms.Form):
    query = forms.CharField(label='Search for a book', max_length=100, required=False)
    genre = forms.ChoiceField(
        choices=[('', 'Select a genre (optional)')] + Book.Genre_Choices,
        required=False,
        label='Genre'
    )