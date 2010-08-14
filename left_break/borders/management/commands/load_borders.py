import os
from django.contrib.gis.geos import fromstr
from django.contrib.gis.gdal import DataSource
from django.core.management.base import NoArgsCommand
from left_break.borders.models import StateBorder
from left_break import borders

SHP_FILE = os.path.join(os.path.dirname(borders.__file__), "data/statesp020.shp")

class Command(NoArgsCommand):
    help = "Loads all state borders into the datebase"

    def handle(self, **options):
        ds = DataSource(SHP_FILE)
        lyr = ds[0]
        for feature in lyr:
            kwargs = {}
            for field in feature.fields:
                kwargs[field.lower()] = feature[field.lower()].value
            kwargs['geom'] = fromstr(feature.geom.wkt)
            border, created = StateBorder.objects.get_or_create(**kwargs)
            if created:
                print "Created state border for %s" % border.state
