from django.db import models
import uuid


class BatteryCell(models.Model):

    cell_id = models.CharField(max_length=10, unique=True, primary_key=True)
    barcode_image_url = models.URLField(max_length=200, blank=True, null=True)
    image_url = models.URLField(max_length=200, blank=True, null=True)

    condition = models.CharField(max_length=20, choices=[
        ('new', 'new'),
        ('recycled', 'recycled'),
    ], default='new')
    manufacturer = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    battery_type = models.CharField(max_length=100)
    form_factor = models.CharField(max_length=100)
    mass = models.FloatField(default=0.0)
    height = models.FloatField(default=0.0)
    diameter = models.FloatField(default=0.0)
    volume = models.FloatField(default=0.0)

    # Default electrical parameters
    nominal_voltage = models.FloatField(default=3.6)
    nominal_energy = models.FloatField(default=16.2)
    nominal_charge_capacity = models.FloatField(default=4.5)
    voltage_range = models.CharField(max_length=100, default='2.5-4.2')
    current_continuous = models.FloatField(default=8.61)
    current_peak = models.FloatField(default=17.5)
    power_continuous = models.FloatField(default=25.6)
    power_peak = models.FloatField(default=50.0)
    energy_density_gravimetric = models.FloatField(default=154)
    energy_density_volumetric = models.FloatField(default=375)
    power_density_gravimetric = models.FloatField(default=837)
    power_density_volumetric = models.FloatField(default=2.04)

    def __str__(self):
        return self.manufacturer + ' ' + self.model
