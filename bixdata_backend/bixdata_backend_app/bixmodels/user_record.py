from django.contrib.sessions.models import Session
import os
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.http import HttpResponse
from django.template.loader import render_to_string
import requests
import json
import datetime
from django.contrib.auth.decorators import login_required
import time
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.db import connection, connections
from django.http import JsonResponse
from django.contrib.auth.models import Group, Permission, User, Group
from django_user_agents.utils import get_user_agent
#from bixdata_app.models import MyModel
from django import template
from bs4 import BeautifulSoup
from django.db.models import OuterRef, Subquery

bixdata_server = os.environ.get('BIXDATA_SERVER')

class UserRecord:
    
    def __init__(self, tableid, recordid=None, userid=1):
        self.tableid=tableid
        self.recordid=recordid
        self.userid=userid
        self.master_tableid=''
        self.master_recordid=''
        self.context='insert_fields'
        if recordid:
            self.fields=self.db_helper.sql_query_row(f"SELECT * FROM user_{self.tableid} WHERE recordid_='{self.recordid}'")
        else:
            self.fields=dict()
    