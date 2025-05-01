from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse, reverse_lazy

from .models import Book, MainMenu, CartItem
from .forms import BookForm, BookSearchForm


def index(request):
    return render(request, 'bookMng/index.html', {
        'item_list': MainMenu.objects.all()
    })


def postbook(request):
    submitted = False
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.username = request.user
            book.save()
            return HttpResponseRedirect('/postbook?submitted=True')
    else:
        form = BookForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'bookMng/postbook.html', {
        'form': form,
        'submitted': submitted,
        'item_list': MainMenu.objects.all()
    })


def displaybooks(request):
    books = Book.objects.all()
    return render(request, 'bookMng/displaybooks.html', {
        'item_list': MainMenu.objects.all(),
        'books': books,
    })


@login_required
def mybooks(request):
    books = Book.objects.filter(username=request.user)
    return render(request, 'bookMng/mybooks.html', {
        'item_list': MainMenu.objects.all(),
        'books': books,
    })


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'bookMng/book_detail.html', {
        'item_list': MainMenu.objects.all(),
        'book': book
    })


def book_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return render(request, 'bookMng/book_delete.html', {
        'item_list': MainMenu.objects.all(),
    })


class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)


def search_book(request):
    form = BookSearchForm(request.GET or None)
    results = Book.objects.none()

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
    favorite_books = []
    if request.user.is_authenticated:
        favorite_books = request.user.favorite_books.all()

    return render(request, 'bookMng/favorites.html', {
        'item_list': MainMenu.objects.all(),
        'books': favorite_books
    })


def toggle_favorite(request, book_id):
    if not request.user.is_authenticated:
        return redirect_to_login(request.get_full_path())

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


def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.book.price * item.quantity for item in cart_items)
    return render(request, "bookMng/my_cart.html", {
        "cart_items": cart_items,
        "total_price": total_price,
        "item_list": MainMenu.objects.all(),
    })


def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, book=book)

    if created:
        cart_item.quantity = 1
    else:
        cart_item.quantity += 1

    cart_item.save()
    return redirect('displaybooks')


def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('my_cart')
