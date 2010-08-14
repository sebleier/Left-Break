from django.contrib.gis.db import models


class Buoy(models.Model):
    name = models.CharField(max_length=50)
    point = models.PointField(srid=4326)

    objects = models.GeoManager()

    def __unicode__(self):
        return u"<Buoy %s>" % self.name
