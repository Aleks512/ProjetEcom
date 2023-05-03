from django.forms import PasswordInput
from django.shortcuts import render
from django.views import generic
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import ConsultantCreationForm, CustomerCreationForm
from .models import Consultant, Customer
from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import UserPassesTestMixin



def home(request):

    return render(request, "users/home.html")

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

class ConsultantDelete(UserPassesTestMixin, DeleteView):
        model = Consultant
        template_name = "users/consultant_delete_form.html"
        fields = '__all__'
        def get_success_url(self):
            return '/consultant/list'

        def test_func(self):
            # Vérifier si l'utilisateur en cours est authentifié et superutilisateur
            return self.request.user.is_authenticated and self.request.user.is_superuser

class AdminHomePageView(TemplateView):
    template_name = "users/home_admin.html"
