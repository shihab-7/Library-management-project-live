from django.urls import path
from .views import DepositeMoneyView,return_view,borrow_view


urlpatterns = [
    path('deposite/',DepositeMoneyView.as_view(), name='deposite'),
    path('borrow/<int:id>/',borrow_view, name='borrow'),
    path('return/<int:id>/',return_view, name='return'),
]
