from django.urls import path, include
from . import views

urlpatterns=[
    path("consultant/add/", views.ConsultantCreateView.as_view(), name="consultant-add"),
    path("consultant/list/", views.ConsultantListView.as_view(), name="consultant-list"),
    path("inscription/",  views.SignUp.as_view(), name="signup")
]
