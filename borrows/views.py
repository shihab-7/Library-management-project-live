from django.shortcuts import render, redirect
from .forms import DepositeForm
from .models import Transaction
from .constants import TRANSACTION_TYPE , DEPOSITE, BORROW,RETURN
from django.views.generic import CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from books.models import Book
from accounts.models import UserLibraryAccount
from django.contrib.auth.decorators import login_required
# Create your views here.


def send_transaction_email(user, amount, subject, template):
    # print(user.email)
    message = render_to_string(template, {
        'user' : user,
        'amount' : amount,
    })

    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()


class TransactionCreateMixin(LoginRequiredMixin, CreateView):

    template_name = 'transaction_form.html'
    model = Transaction
    title = ''
    success_url = reverse_lazy('profile')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account' : self.request.user.account,
        })

        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title' : self.title,
        })
        return context



class DepositeMoneyView(TransactionCreateMixin):
    form_class = DepositeForm
    title = 'Deposite Money'

    def get_initial(self):
        initial = {'transaction_type': DEPOSITE}
        return initial
    
    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        account.balance += amount
        print(self.request.user)

        account.save(
            update_fields = ['balance']
        )

        messages.success(self.request, f'{amount} $ is deposited successfully in your account')

        send_transaction_email(self.request.user, amount, "Deposite Message", "deposite_email.html")
         
        return super().form_valid(form)


@login_required
def borrow_view(request, id):
    user = request.user
    user_account = UserLibraryAccount.objects.filter(user=user).first()
    book = Book.objects.get(id=id)

    if book.price > user_account.balance:
        messages.error(request, 'You DO not have enough Money')
        return redirect('homepage')
    else:
        user_account.balance -= book.price
        user_account.save()

        Transaction.objects.create(
            account = user_account,
            amount = book.price,
            balance_after_transaction = user_account.balance,
            transaction_type = BORROW
        )
        messages.success(request, 'Book borrowed successfully')
        book.borrowing_users.add(user)
        # send mail
        send_transaction_email(user, book.price, "Borrow Message", "borrow_email.html")
        return redirect('profile')

@login_required   
def return_view(request, id):
    user = request.user
    user_account = UserLibraryAccount.objects.filter(user=user).first()
    book = Book.objects.get(id=id)

    user_account.balance += book.price
    user_account.save()

    Transaction.objects.create(
            account = user_account,
            amount = book.price,
            balance_after_transaction = user_account.balance,
            transaction_type = RETURN
        )
    book.borrowing_users.remove(user)
    messages.success(request, 'Book returned successfully')
    return redirect('profile')
