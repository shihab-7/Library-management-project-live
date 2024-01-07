from django.db import models
from django.contrib.auth.models import User
from django.db import models
from categories.models import Category

# Create your models here.
class Book(models.Model):
    category = models.ManyToManyField(Category) #one book can have many categories
    title = models.CharField(max_length=100)
    Description = models.TextField(max_length=200)
    image = models.ImageField(upload_to= 'books/', blank=True, null=True)
    price = models.DecimalField(max_digits=4 , decimal_places= 2)
    borrowing_users = models.ManyToManyField(User, related_name='borrow_history', blank=True)

    def __str__(self):
        return f'Book title : {self.title}'
    
class Reviews(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=40)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reviewed by {self.name}"