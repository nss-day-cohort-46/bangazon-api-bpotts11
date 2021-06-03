from django.urls import path
from .views import completedorder_list, incompleteorder_list

urlpatterns = [
    path('reports/completedorders', completedorder_list),
    path('reports/incompleteorders', incompleteorder_list),
]
