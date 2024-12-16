# authentication/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('test/', get_test, name='test'),

]