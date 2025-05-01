from django.db import models
from django.contrib.auth.models import User
#import something check notes for 2/19

# Create your models here.


class MainMenu(models.Model):
    item = models.CharField(max_length=300, unique=True)
    link = models.CharField(max_length=300, unique=True)

    def __str__(self):
        return self.item

class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=100, blank=True)
    publisher = models.CharField(max_length=100, blank=True)
    year = models.PositiveIntegerField(blank=True, null=True)
    isbn = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)

    web = models.URLField(max_length=300)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    publishdate = models.DateField(auto_now=True)
    picture = models.ImageField(upload_to='uploads/')
    username = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    favorites = models.ManyToManyField(User, related_name="favorite_books", blank=True)

    Genre_Choices = [
        ('Fiction', 'Fiction'),
        ('Nonfiction', 'Nonfiction'),
        ('Mystery', 'Mystery'),
        ('Fantasy', 'Fantasy'),
        ('Other', 'Other'),
    ]

    genre = models.CharField(max_length=50, choices=Genre_Choices, default='Other')

    def __str__(self):
        return self.name

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.book.name}"


class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    def display_user(self):
        return self.user.username if self.user else "Anonymous"

    def __str__(self):
        return f"{self.display_user()} - {self.rating}★"

