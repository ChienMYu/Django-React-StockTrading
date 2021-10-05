from django.urls import path 
from . import views 
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('login/', obtain_auth_token, name='api-login'),
    path('register/', views.register, name='api-register'),
    path('stocks/transaction', views.stockTransaction, name="api-stockTransaction"),
    path('stocks/getHistory', views.getStockHistory, name="api-getStockHistory"),
    path('stocks/myStocks', views.getMyStock, name="api-getMyStocks"),
    path('profile/', views.getAccount, name="api-getAccount"),
   
]