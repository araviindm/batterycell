from django.urls import path
from .views import battery_cell

urlpatterns = [
    path('batterycell/', battery_cell, name='batterycell-view'),
    path('batterycell/', battery_cell,
         name='batterycell-create'),
]
