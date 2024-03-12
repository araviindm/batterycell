from django.db import models


class BatteryCell(models.Model):

    cell_id = models.CharField(
        max_length=36, editable=False, unique=True, primary_key=True)
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

    nominal_voltage = models.FloatField()
    nominal_energy = models.FloatField()
    nominal_charge_capacity = models.FloatField()
    voltage_range = models.CharField(max_length=100)
    current_continuous = models.FloatField()
    current_peak = models.FloatField()
    power_continuous = models.FloatField()
    power_peak = models.FloatField()
    energy_density_gravimetric = models.FloatField()
    energy_density_volumetric = models.FloatField()
    power_density_gravimetric = models.FloatField()
    power_density_volumetric = models.FloatField()

    def __str__(self):
        return self.manufacturer + ' ' + self.model
