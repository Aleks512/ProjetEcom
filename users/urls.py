from django.urls import path, include
from . import views

urlpatterns=[
    path("consultant/add/", views.ConsultantCreationView.as_view(), name="consultant-add"),
]
