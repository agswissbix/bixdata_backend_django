from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from ..bixlogic.bixdata_logic import *

@login_required
def get_menu_items(request):
    menu_items_dict=BixdataLogic.get_menu_items()
    return JsonResponse(menu_items_dict)


@csrf_exempt
def get_sidebarmenu_items(request):
    tables=SysTable.get_user_tables(1)
    workspaces_tables=dict()
    for table in tables:
        workspace = table["workspace"]
        
        if workspace not in workspaces_tables:
            workspaces_tables[workspace] = {}
            workspaces_tables[workspace]["id"]=table['workspace']
            workspaces_tables[workspace]["title"]=table['workspace']
            workspaces_tables[workspace]["icon"]='Home'
        subitem={}
        subitem['id']=table['id']
        subitem['title']=table['description']
        subitem['href']="#"
        if "subItems" not in workspaces_tables[workspace]:
            workspaces_tables[workspace]['subItems']=[]
        workspaces_tables[workspace]["subItems"].append(subitem)

    response = {
        "menuItems": workspaces_tables
    }


    return JsonResponse(response, safe=False)

@csrf_exempt
def get_table_records(request):
    if request.method == 'POST':
        try:
            payload = json.loads(request.body)
            tableid=payload['tableid']
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    response = {
            "rows": [
                {
                    "recordid": "1",
                    "css": "#",
                    "fields": [
                        {
                            "recordid": "",
                            "css": "",
                            "type": "standard",
                            "value": "macbook backend"
                        },
                        {
                            "recordid": "",
                            "css": "",
                            "type": "standard",
                            "value": "nero"
                        },
                        {
                            "recordid": "",
                            "css": "",
                            "type": "standard",
                            "value": "Laptop"
                        },
                        {
                            "recordid": "",
                            "css": "",
                            "type": "standard",
                            "value": "2k"
                        },
                    ]
                },
                {
                    "recordid": "2",
                    "css": "#",
                    "fields": [
                        {
                            "recordid": "",
                            "css": "",
                            "type": "standard",
                            "value": "surface"
                        },
                        {
                            "recordid": "",
                            "css": "",
                            "type": "standard",
                            "value": "bianco"
                        },
                        {
                            "recordid": "",
                            "css": "",
                            "type": "standard",
                            "value": "Laptop"
                        },
                        {
                            "recordid": "",
                            "css": "",
                            "type": "standard",
                            "value": "1k"
                        },
                    ]
                },
            ],
            "columns": [
                {
                    "fieldtypeid": "Numero",
                    "desc": "Product name"
                },
                {
                    "fieldtypeid": "Numero",
                    "desc": "Color"
                },
                {
                    "fieldtypeid": "Numero",
                    "desc": "Type"
                },
                {
                    "fieldtypeid": "Numero",
                    "desc": "Price"
                },
            ]
        }


    table=UserTable(tableid)
    rows=table.get_results_records()
    columns=[]
    columns=table.get_results_columns()
    response_columns=[]
    for column in columns:
        response_column={}
        response_column['fieldtypeid']=column['fieldtypeid']
        response_column['desc']=column['description']
        response_columns.append(response_column)

    response_rows=[]
    for row in rows:
        response_row={}
        response_row['recordid']=row['recordid_']
        response_row['css']=''
        response_row['fields']=[]
        for column in columns:
            field={}
            field['type']=""
            field['value']=row[column['fieldid']]
            field['css']=""
            field['linkedmaster_tableid']=""
            field['linkedmaster_recordid']=""
            response_row['fields'].append(field)
        response_rows.append(response_row)
    response['rows']=response_rows
    response['columns']=response_columns
    return JsonResponse(response, safe=False)
