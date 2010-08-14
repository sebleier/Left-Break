import os
from lxml import etree
from django.core.management.base import NoArgsCommand
from django.contrib.gis.geos import Point
from left_break.buoys.models import Buoy
from left_break import buoys

BUOY_STATIONS = os.path.join(os.path.dirname(buoys.__file__), "data/stations.kml")

class Command(NoArgsCommand):
    help = "Loads all buoys into the datebase"

    def handle(self, **options):
        f = open(BUOY_STATIONS)
        kml = etree.fromstring(f.read())
        namespace = 'http://earth.google.com/kml/2.2'
        f.close()
        folders = kml.xpath("//a:Document/a:Folder/a:Folder", namespaces={'a': namespace})
        for folder in folders:
            placemarks = folder.findall("{%s}Placemark" % namespace)
            for placemark in placemarks:
                coords = placemark.find("{%s}Point/{%s}coordinates" % (namespace, namespace)).text.split(",")
                point = Point(float(coords[0]), float(coords[1]), srid=4326)
                name = placemark.find("{%s}name" % namespace).text
                buoy, created = Buoy.objects.get_or_create(name=name, point=point)
                if created:
                    print "Created Buoy: %s -- %s" % (buoy.name, str(buoy.point.coords))
