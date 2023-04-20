from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import ConsultantCreationForm
from .models import Consultant

class ConsultantCreateView(CreateView):
    template_name = 'consultant_create.html'
    form_class = ConsultantCreationForm
    success_url = reverse_lazy('consultant_list')
    model = Consultant
