from django.shortcuts import render
from books.models import Book
from categories.models import Category
def home(request, category_slug=None):
    data = Book.objects.all()
    categories = Category.objects.all()

    if category_slug is not None:
        category = Category.objects.get(slug=category_slug)
        data = Book.objects.filter(category=category)
    
    return render(request, 'home.html',{'data':data, 'categories':categories})