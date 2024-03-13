import json
from matplotlib import pyplot as plt
import numpy as np
import plotly.graph_objects as go
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response

from api.models import BatteryCell
from .serializers import BatteryCellSerializer

import pandas as pd
from impedance.visualization import plot_bode
import matplotlib
matplotlib.use('Agg')


@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser])
def battery_cell(request, format=None):
    if request.method == 'GET':
        try:
            battery_cells = BatteryCell.objects.all()
            serializer = BatteryCellSerializer(battery_cells, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'POST':
        try:
            serializer = BatteryCellSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_battery_cell_by_id(request, id, format=None):
    try:
        battery_cell = BatteryCell.objects.get(pk=id)
    except BatteryCell.DoesNotExist:
        return Response({'error': 'Battery cell not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = BatteryCellSerializer(battery_cell)
    return Response(serializer.data, status=status.HTTP_200_OK)


def generate_plot(frequency, impedance_real, impedance_imag):

    impedance_complex = impedance_real + 1j * impedance_imag

    plt.rcParams['figure.figsize'] = (12, 12)
    bode_plot_data = plot_bode(frequency, impedance_complex)

    # bode_plot_data to plotly data
    plot_data = []
    for ax in bode_plot_data:
        plot_data += convert_to_plotly(ax)

    # Prepare data for plotly to recieve in front-end
    json_plot_data = []
    for trace in plot_data:
        json_trace = {
            'name': trace.name,
            'x': trace.x.tolist(),  # Convert ndarray to list
            'y': trace.y.tolist()   # Convert ndarray to list
        }
        json_plot_data.append(json_trace)
    return json.dumps(json_plot_data)


def convert_to_plotly(ax):
    traces = []
    for line in ax.lines:
        x = line.get_xdata()
        y = line.get_ydata()
        name = line.get_label()
        trace = go.Scatter(x=x, y=y, name=name)
        traces.append(trace)
    return traces


def get_battery_health(impedance_real):

    Rb_current = np.min(impedance_real)
    Rb_max = np.max(impedance_real)
    # Formula
    SoH_percentage = (Rb_current / Rb_max) * 100

    return SoH_percentage


def compute_circuit_parameters(frequency, impedance_real, impedance_imag):
    # Electrolyte resistance
    Rb = np.mean(impedance_real)
    # Resistance due to SEI layer
    R_SEI = np.max(impedance_real) - np.min(impedance_real)
    # Capacitance due to SEI layer
    CPE_SEI = np.std(impedance_imag)
    # Charge-transfer resistance
    R_CT = np.mean(impedance_real) + np.mean(impedance_imag)
    # Double-layer capacitance
    CPE_DL = np.std(impedance_real) + np.std(impedance_imag)
    # Frequency-dependent Warburg impedance
    W_Warburg = np.mean(frequency)

    return {
        'Rb': Rb,
        'R_SEI': R_SEI,
        'CPE_SEI': CPE_SEI,
        'R_CT': R_CT,
        'CPE_DL': CPE_DL,
        'W_Warburg': W_Warburg
    }


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def compute(request):
    if 'file' not in request.FILES:
        return Response({'error': 'File not found'}, status=status.HTTP_400_BAD_REQUEST)

    file = request.FILES['file']

    try:
        # Split the three columns into frequency, impedance_real and impedance_imag
        df = pd.read_csv(file, delimiter="\t", header=None)
        df = df[0].str.split(',', expand=True).astype(float)
        frequency = df.iloc[:, 0].values
        impedance_real = df.iloc[:, 1].values
        impedance_imag = df.iloc[:, 2].values

        plot_data_json = generate_plot(
            frequency, impedance_real, impedance_imag)
        state_of_health = get_battery_health(impedance_real)
        circuit_params = compute_circuit_parameters(
            frequency, impedance_real, impedance_imag)
        return Response([plot_data_json, state_of_health, circuit_params], status=status.HTTP_200_OK)
    except Exception as e:

        return Response({'error': str(e)}, status=status.HTTP_202_ACCEPTED)
