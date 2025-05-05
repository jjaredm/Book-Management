from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse, reverse_lazy
from .models import Comment
from .forms import CommentForm

from .models import Book, MainMenu, CartItem
from .forms import BookForm, BookSearchForm


from .models import Book

from django.db.models import Avg
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import CartItem



def index(request):
    top_books = Book.objects.all()[:3]  # Or use custom logic for "top"
    return render(request, 'bookMng/index.html', {
        'item_list': MainMenu.objects.all(),
        'top_books': top_books
    })


@login_required()
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
    sort = request.GET.get("sort")
    show_favorites = request.GET.get("fav") == "1"

    books = Book.objects.annotate(avg_rating=Avg('comments__rating'))

    if show_favorites and request.user.is_authenticated:
        books = books.filter(favorites=request.user)

    if sort == "price_asc":
        books = books.order_by("price")
    elif sort == "price_desc":
        books = books.order_by("-price")
    elif sort == "name":
        books = books.order_by("name")
    elif sort == "new":
        books = books.order_by("-publishdate")

    paginator = Paginator(books, 6)
    page_number = request.GET.get("page")

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'bookMng/displaybooks.html', {
        'item_list': MainMenu.objects.all(),
        'books': page_obj,
        'request': request
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
    comments = book.comments.order_by('-created_at')

    # Fetch related books by genre (excluding the current book)
    related_books = Book.objects.filter(genre=book.genre).exclude(id=book.id)[:3]

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.book = book
            comment.user = request.user if request.user.is_authenticated else None
            comment.save()
            return redirect('book_detail', book_id=book.id)
    else:
        form = CommentForm()

    return render(request, 'bookMng/book_detail.html', {
        'item_list': MainMenu.objects.all(),
        'book': book,
        'form': form,
        'comments': comments,
        'related_books': related_books,  # ← ADD THIS
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



def search_books(request):
    query = request.GET.get('q')
    results = Book.objects.filter(name__icontains=query) if query else []
    return render(request, 'bookMng/search_results.html', {
        'results': results,
        'query': query
    })


@login_required
def favorites(request):
    books = Book.objects.filter(favorites=request.user)
    return render(request, 'bookMng/favorites.html', {'books': books})


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
    format = request.POST.get('format', 'Unknown')  # Get selected format

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        book=book,
        defaults={'format': format}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('displaybooks')



def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('my_cart')

def about(request):
    return render(request, 'bookMng/about.html')


@login_required
def update_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)

    if request.method == 'POST':
        new_format = request.POST.get('format')
        new_quantity = request.POST.get('quantity')

        if new_format in ['Physical', 'Digital', 'Audio']:
            item.format = new_format

        if new_quantity.isdigit() and int(new_quantity) > 0:
            item.quantity = int(new_quantity)

        item.save()

    return redirect('my_cart')
