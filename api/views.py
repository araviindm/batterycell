from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response

from api.models import BatteryCell
from .serializers import BatteryCellSerializer


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
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
