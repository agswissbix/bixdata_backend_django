from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def get_testget(request,menuitem='test'):
    #data = json.loads(request.body)
    #menuItem = 'test'#data.get("menuItem")
    response_data = {
        "userId": 1,
        "name": "John BixDoe2",
        "email": "johndoe@example.com",
        "menuItemBackend": menuitem+"-Backend"
    }
    return JsonResponse(response_data)

@csrf_exempt
def get_testpost(request):    
    if request.method == 'POST':
        try:
            # Decodifica il corpo della richiesta JSON
            data = json.loads(request.body)
            selectedMenu1 = data.get('selectedMenu1')

            # Crea una risposta basata sui dati ricevuti
            response_data = {
                "userId": 1,
                "name": "John BixDoe2",
                "email": "johndoe@example.com",
                "menuItemBackend": f"{selectedMenu1}-Backend" if selectedMenu1 else "No Menu Item"
            }
            return JsonResponse(response_data)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
    

def get_menu(request):
# Declare the array
    menu_array = [
        {
            "id": "home",
            "title": "Home",
            "icon": "Home",  # Replace with the actual React component if needed
            "href": "#",
        },
        {
            "id": "prodotti",
            "title": "Prodotti",
            "icon": "Package",  # Replace with the actual React component if needed
            "subItems": [
                {"id": "cat1", "title": "Categoria 1", "href": "#"},
                {"id": "cat2", "title": "Categoria 2", "href": "#"},
                {"id": "cat3", "title": "Categoria 3", "href": "#"},
                {"id": "cat4", "title": "Categoria 4", "href": "#"},
            ],
        },
        {
            "id": "contatti",
            "title": "Contatti",
            "icon": "Mail",  # Replace with the actual React component if needed
            "href": "#",
        },
    ]

    # Convert the array to JSON
    response_data = {
        "userId": 1,
        "name": "John BixDoe",
        "email": "johndoe@example.com"
    }
    return JsonResponse(response_data)

  
    #return HttpResponse(menu_json)
    