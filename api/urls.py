from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views, customer_views, consultant_views
from api.serializers import CustomTokenObtainPairSerializer
from api.views import CommentListAPIView, CommentDetailAPIView
from .consultant_views import ClientListAPIView, ConsultantSendMessageAPIView
from .customer_views import OrderListAPIView, OrderDetailAPIView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/', TokenObtainPairView.as_view(serializer_class=CustomTokenObtainPairSerializer), name='token_obtain_pair'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),#browsable login
    path('orders/', views.OrderList.as_view(), name='order-list'),
    #Customer API
    path('customer/consultant/', customer_views.view_customer_consultant, name='view_customer_consultant'),
    path('customer/orders/', OrderListAPIView.as_view(), name='order-list'),
    path('customer/orders/<int:id>/', OrderDetailAPIView.as_view(), name='order-detail'),
    path('cus/comments/', CommentListAPIView.as_view(), name='comment-list'),
    path('cus/comments/<int:id>/', CommentDetailAPIView.as_view(), name='comment-detail'),
    path('customer/messages/send/', customer_views.CustomerSendMessageAPIView.as_view(), name='send_message'),
    #Consultant API
    path('consultant/clients/', ClientListAPIView.as_view(), name='message-create'),
    path('consultant/clients/<int:id>/', ClientListAPIView.as_view(), name='message-create'),
    path('consultant/orders/<int:order_id>/update-status/', consultant_views.consultant_order_update_status, name='update_order_status'),
    path('consultant/send-message/<int:recipient_id>/', ConsultantSendMessageAPIView.as_view(), name='consultant-send-message'),
]


