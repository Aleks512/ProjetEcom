from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from . import views

urlpatterns=[
    path('', views.home, name="home"),
    path('login/', LoginView.as_view(template_name='registration/login.html',redirect_authenticated_user=True), name = 'login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("consultant/add/", views.ConsultantCreateView.as_view(), name="consultant-add"),
    path("consultants/list/", views.ConsultantListView.as_view(), name="consultant-list"),
    path("customer/inscription/",  views.SignUp.as_view(), name="signup"),
    path('customers/list/', views.CustomerListView.as_view(), name='customers-list')
]
