from .models import CartItem
from .models import Book


def cart_item_count(request):
    if request.user.is_authenticated:
        return {'cart_item_count': CartItem.objects.filter(user=request.user).count()}
    return {'cart_item_count': 0}

def favorite_count(request):
    if request.user.is_authenticated:
        return {'favorite_count': Book.objects.filter(favorites=request.user).count()}
    return {'favorite_count': 0}
