from django.urls import path, include
from . import views

urlpatterns=[
    path("consultant/add/", views.ConsultantCreateView.as_view(), name="consultant-add"),
    path("consultants/list/", views.ConsultantListView.as_view(), name="consultant-list"),
    path("customer/inscription/",  views.SignUp.as_view(), name="signup"),
    path('customers/list/', views.CustomerListView.as_view(), name='customers-list')
]
