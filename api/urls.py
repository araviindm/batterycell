from django.urls import path
from .views import battery_cell, get_battery_cell_by_id, generate_plot

urlpatterns = [
    path('batterycell', battery_cell, name='batterycell'),
    path('batterycell/<str:id>', get_battery_cell_by_id,
         name='batterycell-detail'),
    path('impedance/plot', generate_plot, name='generate_plot'),
]
