# authentication/urls.py
from django.urls import path
from .views import *
from .views import csrf_token_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('csrf-token/', csrf_token_view, name='csrf_token'),
    path('home/', home_view, name='home'),
    path('get_sidebar_data/', get_sidebar_data, name='get_sidebar_data'),
    
    
    
]