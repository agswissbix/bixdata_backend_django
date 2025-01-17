from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from ..bixmodels.sys_table import *
from ..bixmodels.user_record import *
from ..bixmodels.user_table import *



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
    response={}
    if request.method == 'POST':
        try:
            payload = json.loads(request.body)
            tableid=payload['tableid']
            searchterm=payload['searchTerm']
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    


    table=UserTable(tableid)
    rows=table.get_results_records(searchTerm=searchterm)
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

@csrf_exempt
def get_record_badge(request):
    response={}
    if request.method == 'POST':
        try:
            payload = json.loads(request.body)
            tableid=payload['tableid']
            recordid=payload['recordid']
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    badge_items = []
    badge_fields=UserRecord(tableid, recordid).get_record_badge_fields()

    response['badgeItems']=badge_fields
    record=UserRecord(tableid)

    return JsonResponse(response, safe=False)

@csrf_exempt
def set_record_fields(request):
    if request.method == 'POST':
        try:
            payload = json.loads(request.body)
            print('Payload ricevuto:', payload)  # Log per vedere cosa arriva

            tableid = payload['tableid']
            recordid = payload['recordid']
            fields = payload['fields']
            print('TableID:', tableid)
            print('RecordID:', recordid)
            print('Fields:', fields)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except KeyError as e:
            return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
    if tableid=='company':
        record=UserRecord(tableid, recordid)
        record.values['companyname']="Thinstuff s.r.o. test"
        record.save()
    return JsonResponse({'status': 'ok'}, status=200)

@csrf_exempt
def get_record_fields(request):
    response={}
    if request.method == 'POST':
        try:
            payload = json.loads(request.body)
            tableid=payload['tableid']
            recordid=payload['recordid']
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    record=UserRecord(tableid, recordid)
    fields=record.get_fields_detailed()



    response['recordid']=recordid
    response['fields']=fields
    record=UserRecord(tableid)

    return JsonResponse(response, safe=False)