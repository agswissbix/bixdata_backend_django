# authentication/urls.py
from django.urls import path
from .bixviews.authentication_view import *
from .bixviews.bixdata_view import *
from .bixviews.settings_view import *

urlpatterns = [
    path('test_connection/', test_connection , name='login'),
    path('login/', login_view , name='login'),
    path('logout/', logout_view, name='logout'),
    path('csrf-token/', csrf_token_view, name='csrf_token'),
    path('home/', home_view, name='home'),
    path('get_sidebarmenu_items/', get_sidebarmenu_items, name='get_sidebarmenu_items'),
    path('get_table_records/', get_table_records, name='get_table_records'),
    path('get_record_badge/', get_record_badge, name='get_record_badge'),
    path('get_record_fields/', get_record_fields, name='get_record_fields'),
    path('set_record_fields/', set_record_fields, name='set_record_fields'),
    path('create_pdf/', create_pdf, name='create_pdf'),
    path('test_linkedmaster/', test_linkedmaster, name='test_linkedmaster'),
    path('get_user_theme/', get_user_theme, name='get_user_theme'),
    
    
    
    
]