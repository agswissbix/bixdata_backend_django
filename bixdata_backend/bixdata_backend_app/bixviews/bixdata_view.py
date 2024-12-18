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

@login_required
def get_sidebar_data(request):
    workspaces=SysTable.get_workspaces(1)
    menu_items=[]
    for workspace in workspaces:
        workspace_menu_item={
                "id": "home",
                "title": "Home Backend",
                "icon": "Home",  # Replace with the actual React component or Python equivalent
                "href": "#",
            }
        
        menu_items.append(workspace_menu_item)
        menu_items2 = [
            {
                "id": "home",
                "title": "Home Backend",
                "icon": "Home",  # Replace with the actual React component or Python equivalent
                "href": "#",
            },
            {
                "id": "prodotti",
                "title": "Prodotti",
                "icon": "Package",  # Replace with the actual React component or Python equivalent
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
                "icon": "Mail",  # Replace with the actual React component or Python equivalent
                "href": "#",
            },
        ]

    return JsonResponse(menu_items, safe=False)