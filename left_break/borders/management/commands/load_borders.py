import os
from django.contrib.gis.geos import fromstr
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import Point, Polygon, LineString
from django.core.management.base import NoArgsCommand
from left_break.borders.models import StateBorder, Coastline
from left_break import borders

SHP_FILE = os.path.join(os.path.dirname(borders.__file__), "data/statesp020.shp")

bbox = Polygon((
    (-124.208083, 42.000901),
    (-116.798989, 32.69355),
    (-117.123367, 32.535235),
    (-118.759060, 33.958832),
    (-120.720495, 34.332685),
    (-122.926582, 37.718859),
    (-125.048972, 40.717364),
    (-124.208083, 42.000901)),
    srid=4326,
)

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

        # Create California coastline
        coastlines = []
        for border in StateBorder.objects.filter(state__icontains="california"):
            for coords in border.geom.coords:
                points = []
                for lon, lat in coords:
                    point = Point(lon, lat)
                    if bbox.contains(point):
                        points.append(point)
                if points:
                    linestring = LineString(*points)
                    coastlines.append(linestring)

        for coastline in coastlines:
            obj, created = Coastline.objects.get_or_create(state="califonia", geom=coastline)
            if created:
                print "Created Coast for extent: %s" % str(obj.geom.extent)
