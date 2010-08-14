# This is an auto-generated Django model module created by ogrinspect.
from django.contrib.gis.db import models

class StateBorder(models.Model):
    area = models.FloatField()
    perimeter = models.FloatField()
    statesp020 = models.FloatField()
    state = models.CharField(max_length=20)
    state_fips = models.CharField(max_length=2)
    order_adm = models.IntegerField()
    month_adm = models.CharField(max_length=18)
    day_adm = models.FloatField()
    year_adm = models.FloatField()
    geom = models.PolygonField(srid=4326)

    objects = models.GeoManager()
