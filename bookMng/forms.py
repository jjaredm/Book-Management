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
            'picture',
        ]

class BookSearchForm(forms.Form):
    query = forms.CharField(label='Search for a book', max_length=100)
