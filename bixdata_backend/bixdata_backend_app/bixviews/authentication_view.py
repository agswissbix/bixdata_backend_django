from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json



@csrf_exempt
def login_view(request):
    """Gestisce il login degli utenti."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return JsonResponse({"message": "Login successful"})
            else:
                return JsonResponse({"error": "Invalid credentials"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "POST request required"}, status=405)



@csrf_exempt
def logout_view(request):
    """Gestisce il logout degli utenti."""
    logout(request)
    return JsonResponse({"message": "Logged out successfully 2"})

def csrf_token_view(request):
    """Restituisce il token CSRF per il frontend."""
    
    csrf_token = get_token(request)
    print('expected_token: '+csrf_token)
    return JsonResponse({"csrfToken": csrf_token})

@login_required
def check_session(request):
    """Verifica se la sessione dell'utente è attiva."""
    expected_token = get_token(request)
    print('expected_token: '+expected_token)
    # Ottieni il token inviato nella richiesta
    received_token =  request.headers.get('X-CSRFToken')
    print('received_token: '+received_token)
    return JsonResponse({"message": "User is authenticated"})


@login_required
def home_view(request):
    """Una vista protetta, accessibile solo agli utenti autenticati."""
    
    
    # Ottieni il token inviato nella richiesta
    received_token =  request.headers.get('X-CSRFToken')
    print('received_token: '+received_token)
    return JsonResponse({"message": "You have access to this protected resource1"})

@login_required
def test_request(request):
    #time.sleep(1)
    return JsonResponse({"message": "You have access to this protected resource2"})



