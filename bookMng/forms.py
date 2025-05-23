from django import forms
from django.forms import ModelForm
from .models import Book
from .models import Comment


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'name',
            'author',
            'publisher',
            'year',
            'pages',
            'isbn',
            'description',
            'price',
            'picture',
            'genre',
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'publisher': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'web': forms.URLInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'genre': forms.Select(attrs={'class': 'form-control'}),
        }


class BookSearchForm(forms.Form):
    query = forms.CharField(label='Search for a book', max_length=100, required=False)
    genre = forms.ChoiceField(
        choices=[('', 'Select a genre (optional)')] + Book.Genre_Choices,
        required=False,
        label='Genre'
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'rating']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].required = False
        self.fields['rating'].required = False  # This makes rating optional too
