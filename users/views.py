from django.shortcuts import render
from django.views import generic
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import ConsultantCreationForm, CustomerCreationForm
from .models import Consultant, Customer
from django.db import models


def home(request):

    return render(request, "users/home.html")

class ConsultantCreateView(CreateView):
    template_name = 'users/consultant_create.html'
    form_class = ConsultantCreationForm
    success_url = reverse_lazy('consultant-list')
    model = Consultant

class ConsultantListView(ListView):
    model = Consultant
    template_name = 'user/consultant_list.html'

class SignUp(generic.CreateView):
    form_class = CustomerCreationForm
    success_url = reverse_lazy("customers-list")
    template_name = "users/client_signup.html"

class CustomerListView(ListView):
    model = Customer
    template_name = 'users/customers_list.html'
    context_object_name = 'customers'

    def get_queryset(self):
        return Customer.objects.select_related('consultant_applied')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'List of customers'
        return context


class ConsultantListView(ListView):
    model = Consultant
    template_name = 'users/consultant_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(num_clients=models.Count('clients'))
        return queryset

