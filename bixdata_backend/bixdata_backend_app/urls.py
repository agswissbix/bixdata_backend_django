# authentication/urls.py
from django.urls import path
from .bixviews.authentication_view import *
from .bixviews.bixdata_view import *
from .bixviews.settings_view import *

urlpatterns = [
    path('login/', login_view , name='login'),
    path('logout/', logout_view, name='logout'),
    path('csrf-token/', csrf_token_view, name='csrf_token'),
    path('home/', home_view, name='home'),
    path('get_sidebarmenu_items/', get_sidebarmenu_items, name='get_sidebarmenu_items'),
    path('get_table_records/', get_table_records, name='get_table_records')
    
    
    
    
]