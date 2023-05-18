from django.urls import path
from . import views
from .views import MessageList, MessageDetail

urlpatterns = [
    path('anciens/', views.getData),
    path('message/add', views.addData),
    path("messages/", MessageList.as_view(), name="messages_list"),
    path("message/<int:pk>/", MessageDetail.as_view(), name="messages_detail")
]