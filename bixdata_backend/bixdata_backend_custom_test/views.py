from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json

def get_test(request):
    return get_menu(request)

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
        "name": "John Doe",
        "email": "johndoe@example.com"
    }
    return JsonResponse(response_data)

  
    #return HttpResponse(menu_json)
    