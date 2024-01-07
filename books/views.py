from typing import Any
from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book
from .forms import ReviewForm
# Create your views here.

class BookDetailView(DetailView):
    model = Book
    pk_url_kwarg = 'id'
    template_name = 'bookdetails.html'

    def post(self,request , *args, **kwargs):
        review_form = ReviewForm(data=self.request.POST)
        book = self.get_object()

        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.book = book
            new_review.save()
        return self.get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        reviews = book.reviews.all()
        review_form = ReviewForm()
        context['reviews'] = reviews
        context['review_form'] = review_form
        return context