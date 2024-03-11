import os
import uuid
from django.conf import settings
from rest_framework import serializers
from .models import BatteryCell

import firebase_admin
from firebase_admin import credentials, storage

credentials_path = os.path.join(
    settings.BASE_DIR, 'batterycell_service_account_key.json')
cred = credentials.Certificate(credentials_path)

firebase_admin.initialize_app(
    cred, {'storageBucket': 'batterycell-1f682.appspot.com'})


class BatteryCellSerializer(serializers.ModelSerializer):
    barcode_image = serializers.ImageField(required=False)
    image = serializers.ImageField(required=False)

    class Meta:
        model = BatteryCell
        fields = '__all__'

    def create(self, validated_data):
        barcode_image_file = validated_data.pop('barcode_image', None)
        image_file = validated_data.pop('image', None)

        battery_cell = BatteryCell.objects.create(**validated_data)

        if barcode_image_file:
            # Save barcode image to Firebase Storage and get URL
            barcode_image_url = upload_to_firebase_storage(barcode_image_file)
            battery_cell.barcode_image_url = barcode_image_url

        if image_file:
            # Save regular image to Firebase Storage and get URL
            image_url = upload_to_firebase_storage(image_file)
            battery_cell.image_url = image_url

        battery_cell.save()

        return battery_cell


def upload_to_firebase_storage(file):
    filename = file.name
    unique_filename = str(uuid.uuid4())
    _, extension = os.path.splitext(filename)
    filename_with_extension = f"{unique_filename}{extension}"

    bucket = storage.bucket()

    blob = bucket.blob(filename_with_extension)
    blob.upload_from_file(file)
    blob.make_public()

    url = blob.public_url

    return url
