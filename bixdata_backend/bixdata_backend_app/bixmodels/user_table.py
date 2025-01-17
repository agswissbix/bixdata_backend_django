from django.contrib.sessions.models import Session


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
import os
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
from .helper_db import *

bixdata_server = os.environ.get('BIXDATA_SERVER')

class UserTable:
    
    def __init__(self,tableid,userid=1):
        self.tableid=tableid
        self.userid=userid
        self.context=''

    def get_results_records(self,viewid='',searchTerm='', conditions_list=list(),fields=None,offset=0,limit=None,orderby='recordid_ desc'):
        """Ottieni elenco record in base ai parametri di ricerca

        Args:
            viewid (str, optional): vista applicata. Defaults to ''.
            searchTerm (str, optional): termine generico da cercare in tutti i campi. Defaults to ''.
            conditions_list (_type_, optional): condizioni specifiche sui campi. Defaults to list().

        Returns:
            _type_: lista di dict dei risultati
        """ 
        select_fields='*'
        if fields:
            select_fields=''
            for field in fields:
                if select_fields!='':
                    select_fields=select_fields+','
                select_fields=select_fields+field
                
        conditions="deleted_='N'"
        #conditions=conditions+f" AND companyname like '%{searchTerm}%' " 
        for condition in conditions_list:
            conditions=conditions+f" AND {condition}"   

        sql=f"SELECT {select_fields} from user_{self.tableid} where {conditions} ORDER BY {orderby} LIMIT 10"
        records = HelpderDB.sql_query(sql)
        return records
    
    def get_results_columns(self):
        sql=f"""
            SELECT
            sys_user_order.userid,
            sys_user_order.tableid,
            sys_user_order.fieldid,
            sys_user_order.fieldorder,
            sys_user_order.typepreference,
            sys_field.fieldtypeid,
            sys_field.description,
            sys_field.fieldtypewebid,
            sys_field.tablelink,
            sys_field.keyfieldlink
            FROM sys_user_order
            INNER JOIN sys_field
                ON sys_user_order.tableid = sys_field.tableid
                AND sys_user_order.fieldid = sys_field.fieldid
            WHERE sys_user_order.typepreference = 'risultatiricerca'
            AND sys_user_order.tableid = '{self.tableid}'
            AND sys_user_order.userid = {self.userid}
            ORDER BY sys_user_order.fieldorder
            """
        columns=HelpderDB.sql_query(sql)
        return columns