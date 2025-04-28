from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('postbook', views.postbook, name='postbook'),
    path('displaybooks', views.displaybooks, name='displaybooks'),
    path('mybooks', views.mybooks, name='mybooks'),
    path('search/', views.search_book, name='search_book'),
    path('book_detail/<int:book_id>', views.book_detail, name='book_detail'),
    path('book_delete/<int:book_id>', views.book_delete, name='book_delete'),
    path('favorites/', views.favorites, name='favorites'),
    path('favorite/<int:book_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('users/', views.users, name='users'),

    path('add/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('my_cart/', views.view_cart, name='my_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),







]

