from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import MainMenu
from .models import Book
from .forms import BookForm
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .forms import BookSearchForm

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User

from django.urls import reverse



# Create your views here.


def index(request):
    return render(request, 'bookMng/index.html',
                  {
                      'item_list': MainMenu.objects.all()
                  }
                  )

def postbook(request):
    submitted = False
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save()
            book = form.save(commit=False)
            try:
                book.username = request.user
            except Exception:
                pass
            book.save()
            return HttpResponseRedirect('postbook?submitted=True')
    else:
        form = BookForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request,
                  'bookMng/postbook.html',
                  {
                      'form': form,
                      'item_list': MainMenu.objects.all(),
                      'submitted': submitted
                  }
                  )

def displaybooks(request):
    books = Book.objects.all()
    for b in books:
        b.pic_path = b.picture.url[14:]
    return render(request, 'bookMng/displaybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books,
                  }
                  )
@login_required
def mybooks(request):
    books = Book.objects.filter(username=request.user)
    for b in books:
        b.pic_path = b.picture.url[14:]
    return render(request, 'bookMng/mybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books,
                  }
                  )

def book_detail(request, book_id):

    book = Book.objects.get(id=book_id)
    book.pic_path = book.picture.url[14:]

    return render(request,
                  'bookMng/book_detail.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'book': book
                  }
                  )

def book_delete(request, book_id):

    book = Book.objects.get(id=book_id)
    book.delete()

    return render(request,
                  'bookMng/book_delete.html',
                  {
                      'item_list': MainMenu.objects.all(),
                  }
                  )

class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)

def search_book(request):
    form = BookSearchForm(request.GET or None)
    results = Book.objects.none()  # Start with no results

    if form.is_valid():
        search_term = form.cleaned_data.get('query')
        genre = form.cleaned_data.get('genre')

        if search_term or genre:
            results = Book.objects.all()
            if search_term:
                results = results.filter(name__icontains=search_term)
            if genre:
                results = results.filter(genre=genre)

    return render(request, 'bookMng/search_book.html', {
        'form': form,
        'results': results,
        'item_list': MainMenu.objects.all(),
    })



def favorites(request):
    if not MainMenu.objects.filter(link='/favorites/').exists():
        MainMenu.objects.create(item='Favorites', link='/favorites/')

    favorite_books = []
    if request.user.is_authenticated:
        favorite_books = request.user.favorite_books.all()
        for b in favorite_books:
            b.pic_path = b.picture.url[14:]  # Add this line

    return render(request, 'bookMng/favorites.html', {
        'item_list': MainMenu.objects.all(),
        'books': favorite_books
    })

@login_required
def toggle_favorite(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.user in book.favorites.all():
        book.favorites.remove(request.user)
    else:
        book.favorites.add(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))




@login_required
def users(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'bookMng/users.html', {
        'item_list': MainMenu.objects.all(),
        'users': users
    })

