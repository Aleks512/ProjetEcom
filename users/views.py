from django.views import generic
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import ConsultantCreationForm, ClientCreationForm
from .models import Consultant

class ConsultantCreateView(CreateView):
    template_name = 'users/consultant_create.html'
    form_class = ConsultantCreationForm
    success_url = reverse_lazy('consultant-list')
    model = Consultant

class ConsultantListView(ListView):
    model = Consultant
    template_name = 'user/consultant_list.html'

class SignUp(generic.CreateView):

    form_class = ClientCreationForm
    success_url = reverse_lazy("login")
    template_name = "users/client_signup.html"
