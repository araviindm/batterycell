
import os
import tempfile
import uuid
from django.conf import settings
from rest_framework import serializers
from .models import BatteryCell

from barcode import generate
from barcode.writer import ImageWriter

import firebase_admin
from firebase_admin import credentials, storage

credentials_path = os.path.join(
    settings.BASE_DIR, 'batterycell_service_account_key.json')
cred = credentials.Certificate(credentials_path)

firebase_admin.initialize_app(
    cred, {'storageBucket': 'batterycell-1f682.appspot.com'})


class BatteryCellSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = BatteryCell
        fields = '__all__'

    def create(self, validated_data):
        image_file = validated_data.pop('image', None)

        cell_id = str(uuid.uuid4())
        barcode_image_url = self.generate_barcode_image(cell_id)

        battery_cell = BatteryCell.objects.create(
            cell_id=cell_id,
            barcode_image_url=barcode_image_url,
            **validated_data
        )

        if image_file:
            filename = image_file.name
            unique_filename = str(uuid.uuid4())
            _, extension = os.path.splitext(filename)
            filename_with_extension = f"{unique_filename}{extension}"

            image_url = self.upload_to_firebase_storage(
                image_file, filename_with_extension)
            battery_cell.image_url = image_url

        battery_cell.save()

        return battery_cell

    def generate_barcode_image(self, cell_id):
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            generate('code128', str(cell_id),
                     output=temp_file, writer=ImageWriter())
            temp_file.close()
            with open(temp_file.name, 'rb') as file:
                barcode_image_url = self.upload_to_firebase_storage(
                    file, filename=f'{str(cell_id)}.png')
            return barcode_image_url

    def upload_to_firebase_storage(self, file, filename):
        bucket = storage.bucket()

        blob = bucket.blob(filename)
        blob.upload_from_file(file)
        blob.make_public()

        url = blob.public_url

        return url
