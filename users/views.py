from django.contrib.auth.views import LoginView
from django.forms import PasswordInput
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from eshop.models import Order, Product, Category, Cart
from .forms import ConsultantCreationForm, CustomerCreationForm
from .models import Consultant, Customer, NewUser
from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import UserPassesTestMixin


class WebAppLoginView(LoginView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')  # Replace 'home' with your desired URL after login
        return super().get(request, *args, **kwargs)

def home(request):

    return render(request, "home.html")

def presentation(request):

    return render(request, "presentation.html")

class CustomerHome(UserPassesTestMixin, DetailView):
    model = Customer
    template_name = "users/my_orders.html"
    fields = '__all__'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.customer

    def get_object(self, queryset=None):
        id = self.request.user.customer.id
        return Customer.objects.get(id=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.get_object()
        orders = customer.order_set.all()
        ordered_orders = customer.order_set.filter(ordered=True)
        unordered_orders = customer.order_set.filter(ordered=False)
        context['ordered_orders'] = ordered_orders #querySet
        context['unordered_orders'] = unordered_orders #querySet
        context['orders'] = orders

        return context
class ConsultantHome(UserPassesTestMixin, DetailView):
    model = Consultant
    template_name = "users/home_consultant.html"
    fields = '__all__'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.consultant

    def get_object(self, queryset=None):
        matricule = self.request.user.consultant.matricule
        return Consultant.objects.get(matricule=matricule)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        consultant = self.get_object()
        clients = consultant.clients.all()
        context['clients'] = clients
        return context


class ConsultantCreateView(UserPassesTestMixin,CreateView):
    template_name = 'users/consultant_create.html'
    form_class = ConsultantCreationForm
    success_url = reverse_lazy('consultant-list')
    model = Consultant
    def test_func(self):
        # Vérifier si l'utilisateur en cours est authentifié et superutilisateur
        return self.request.user.is_authenticated and self.request.user.is_superuser
class ConsultantListView(UserPassesTestMixin, ListView):
    model = Consultant
    template_name = 'user/consultant_list.html'
    def test_func(self):
        # Vérifier si l'utilisateur en cours est authentifié et superutilisateur
        return self.request.user.is_authenticated and self.request.user.is_superuser

class SignUp(generic.CreateView):
    form_class = CustomerCreationForm
    success_url = reverse_lazy("login")
    template_name = "users/client_signup.html"

class CustomerListView(UserPassesTestMixin, ListView):
    model = Customer
    template_name = 'users/customers_list.html'
    context_object_name = 'customers'
    def test_func(self):
        # Vérifier si l'utilisateur en cours est authentifié et superutilisateur
        return self.request.user.is_authenticated and self.request.user.is_superuser

    def get_queryset(self):
        return Customer.objects.select_related('consultant_applied')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Clients'
        return context


class ConsultantListView(UserPassesTestMixin, ListView):
    model = Consultant
    template_name = 'users/consultant_list.html'
    def test_func(self):
        # Vérifier si l'utilisateur en cours est authentifié et superutilisateur
        return self.request.user.is_authenticated and self.request.user.is_superuser

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(num_clients=models.Count('clients'))
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Consultants de VentAlis'
        return context

class ConsultantUpdate(UserPassesTestMixin, UpdateView):
    model = Consultant
    template_name = "users/consultant_update_form.html"
    fields = ['email', 'password', 'first_name', 'last_name', 'company']
    widgets = {
        'password': PasswordInput()
    }
    def form_valid(self, form):
        form.instance.password = make_password(form.cleaned_data['password'])
        return super().form_valid(form)
    def test_func(self):
        # Vérifier si l'utilisateur en cours est authentifié et superutilisateur
        return self.request.user.is_authenticated and self.request.user.is_superuser

    def get_success_url(self):
        return '/consultants/list/'

class ConsultantDelete(UserPassesTestMixin, DeleteView):
        model = Consultant
        template_name = "users/consultant_delete_form.html"
        fields = '__all__'
        def get_success_url(self):
            return '/consultants/list/'

        def test_func(self):
            # Vérifier si l'utilisateur en cours est authentifié et superutilisateur
            return self.request.user.is_authenticated and self.request.user.is_superuser

class AdminHomePageView(TemplateView):
    template_name = "users/home_admin.html"