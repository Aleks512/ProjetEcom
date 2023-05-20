from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.serializers import CustomTokenObtainPairSerializer
from api.views import  OrderListAPIView, OrderDetailAPIView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/', TokenObtainPairView.as_view(serializer_class=CustomTokenObtainPairSerializer), name='token_obtain_pair'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),#browsable login
    #path('orders/', views.OrderList.as_view(), name='order-list'),
    path('orders/', OrderListAPIView.as_view(), name='order-list'),
    path('orders/<int:id>/', OrderDetailAPIView.as_view(), name='order-detail'),
]