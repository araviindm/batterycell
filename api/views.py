import base64
import io
import os
import matplotlib.pyplot as plt
import numpy as np
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


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def generate_plot(request):
    if 'file' not in request.FILES:
        return Response({'error': 'File not found'}, status=status.HTTP_400_BAD_REQUEST)

    file = request.FILES['file']

    try:
        df = pd.read_csv(file, sep='\t', header=None)
        df = df[0].str.split(',', expand=True).astype(float)
        frequency = df.iloc[:, 0].values
        impedance_real = df.iloc[:, 1].values
        impedance_imag = df.iloc[:, 2].values

        impedance_complex = impedance_real + 1j * impedance_imag

        plt.rcParams['figure.figsize'] = (10, 10)
        plot_bode(frequency, impedance_complex)

        plt.xlabel('Frequency')
        plt.ylabel('Impedance')

        plt.savefig('bode_plot.png')
        plt.close()

        with open('bode_plot.png', 'rb') as image_file:
            plot_image_base64 = base64.b64encode(
                image_file.read()).decode('utf-8')
        os.remove('bode_plot.png')
        return Response({'plot': plot_image_base64}, status=status.HTTP_200_OK)
    except Exception as e:

        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
