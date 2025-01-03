from django.urls import path
from .views import *

urlpatterns = [
    path('testget/<str:menuitem>/', get_testget, name='testget'), 
    path('testpost/', get_testpost, name='testpost'),
]
