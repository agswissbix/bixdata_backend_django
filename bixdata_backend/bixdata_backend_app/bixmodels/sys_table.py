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
from django import template
from bs4 import BeautifulSoup
from django.db.models import OuterRef, Subquery
from .helper_db import *


class SysTable:
    
    @classmethod
    def get_workspaces(cls,userid):
        sql="SELECT * FROM sys_table_workspace"
        result=HelpderDB.sql_query(sql)
        return result
    
    @classmethod
    def get_user_tables(cls,userid):
        sql="""
            SELECT
            sys_table.id,
            sys_table.description,
            sys_user_table_order.userid,
            sys_table.workspace,
            sys_table_workspace.`order`,
            sys_table_workspace.icon
            FROM sys_table
            INNER JOIN sys_user_table_order
                ON sys_table.id = sys_user_table_order.tableid
            INNER JOIN sys_table_workspace
                ON sys_table.workspace = sys_table_workspace.name
            WHERE sys_user_table_order.userid = 1
            ORDER BY sys_table_workspace.`order`, sys_table.id
        """
        rows=HelpderDB.sql_query(sql)
        return rows
    
        