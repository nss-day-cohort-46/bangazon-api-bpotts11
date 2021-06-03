from django.urls import path
from .views import completedorder_list

urlpatterns = [
    path('reports/completedorders', completedorder_list),
]
