from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from ..bixmodels.sys_table import *
from ..bixmodels.user_record import *
from ..bixmodels.user_table import *
import pdfkit



@csrf_exempt
def test_connection(request):
    response = {
        "Stato": "Connessione riuscita",
    }
    return JsonResponse(response, safe=False)

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
    badge_fields = []
    if not Helper.isempty(recordid):
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


@csrf_exempt
def get_record_linked_tables(request):
    response={}
    if request.method == 'POST':
        try:
            payload = json.loads(request.body)
            tableid=payload['tableid']
            recordid=payload['recordid']
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    record=UserRecord(tableid, recordid)
    linked_tables=record.get_linked_tables()
    response['linkedTables']=linked_tables

    return JsonResponse(response, safe=False)

@csrf_exempt
def create_pdf(request):
    try:
        # Configura il percorso di wkhtmltopdf
        script_dir = os.path.dirname(os.path.abspath(__file__))
        wkhtmltopdf_path = os.path.join(script_dir, 'wkhtmltopdf.exe')
        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

        # Contenuto HTML per il PDF
        content = "<div>TEST</div>"
        row={}
        content = render_to_string('pdf/gasoli.html', row)

        # Genera il percorso del file PDF
        filename_with_path = os.path.join(os.path.dirname(script_dir), 'static', 'pdf', 'test.pdf')

        # Genera il PDF dal contenuto HTML
        pdfkit.from_string(content, filename_with_path, configuration=config, options={"enable-local-file-access": ""})

        # Leggi il file PDF e restituiscilo come risposta
        with open(filename_with_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'inline; filename=test.pdf'
        
        return response

    except Exception as e:
        # In caso di errore, restituisci un errore
        return JsonResponse({'error': str(e)}, status=500)

    finally:
        # Rimuovi il file PDF temporaneo, se esiste
        if os.path.exists(filename_with_path):
            os.remove(filename_with_path)


from ..bixmodels.helper_db import *
@csrf_exempt
def test_linkedmaster(request):
    print('ok reach django')
    response={}
    if request.method == 'POST':
        try:
            payload = json.loads(request.body)
            tableid=payload['tableid']
            tableid= f"user_{tableid}"
            tableid = str(tableid)
            with connection.cursor() as cursor:
                query = f"SELECT recordid_, name FROM {tableid} WHERE name LIKE %s"
                cursor.execute(query, [f"%{payload['searchTerm']}%"])
                rows = HelpderDB.dictfetchall(cursor)
            print(rows)                
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse(rows, safe=False)

@csrf_exempt
def get_user_theme(request):
    response={}
    try:
        payload = json.loads(request.body)
        userid=payload['userid']
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM v_sys_user_settings WHERE bixid = %s and setting='theme'", [userid])
            theme = HelpderDB.dictfetchall(cursor)
            theme = theme[0]['value']
            response['theme'] = theme
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    return JsonResponse(response['theme'], safe=False)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import pyotp
import qrcode
import base64
from io import BytesIO

@csrf_exempt
@login_required
def enable_2fa(request):
    user = request.user
    
    if request.method != "POST":
        return JsonResponse({"message": "Metodo non permesso"}, status=405)

    # Controlla se il 2FA è già attivo
    if request.session.get("otp_secret"):
        return JsonResponse({"message": "2FA già attivato"}, status=400)

    try:
        # Genera un segreto OTP per l'utente
        secret = pyotp.random_base32()
        request.session["otp_secret"] = secret
        request.session.save()

        # Genera l'URL del QR Code
        totp = pyotp.TOTP(secret)
        otp_url = totp.provisioning_uri(name=user.username, issuer_name="MyApp")

        # Genera il QR Code e convertilo in base64
        img = qrcode.make(otp_url)
        img_io = BytesIO()
        img.save(img_io, format="PNG")
        qr_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

        return JsonResponse({"otp_url": otp_url, "qr_code": qr_base64})

    except Exception as e:
        return JsonResponse({"message": f"Errore nel generare il QR: {str(e)}"}, status=500)



@csrf_exempt
@login_required
def verify_2fa(request):
    if request.method != "POST":
        return JsonResponse({"message": "Metodo non permesso"}, status=405)

    # Ottieni i dati JSON
    data = json.loads(request.body)
    otp_token = data.get("otp")
    
    if not otp_token:
        return JsonResponse({"message": "Codice OTP mancante"}, status=400)
    
    secret = request.session.get("otp_secret")
    if not secret:
        return JsonResponse({"message": "2FA non attivato per questo utente"}, status=400)

    totp = pyotp.TOTP(secret)
    if totp.verify(otp_token):
        return JsonResponse({"message": "Autenticazione 2FA riuscita"})
    else:
        return JsonResponse({"message": "Codice OTP errato"}, status=400)
    

@csrf_exempt
@login_required
def disable_2fa(request):
    if request.method != "POST":
        return JsonResponse({"message": "Metodo non permesso"}, status=405)
    
    # Controlla se il 2FA è attivo
    if not request.session.get("otp_secret"):
        return JsonResponse({"message": "2FA non è attivo per questo utente"}, status=400)

    # Rimuovi il segreto dalla sessione
    del request.session["otp_secret"]
    request.session.save()
    
    return JsonResponse({"message": "2FA disabilitato con successo"})

