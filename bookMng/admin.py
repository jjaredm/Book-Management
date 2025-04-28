from django.contrib import admin
from .models import MainMenu
from .models import Book
from .models import CartItem
# Register your models here.

admin.site.register(MainMenu)
admin.site.register(Book)
admin.site.register(CartItem)
