from django.contrib.gis.geos import Polygon
from left_break.decorators import json_view
from left_break.buoys.models import Buoy

@json_view
def buoys(request):
    poly = Polygon((
        (-170.0, 0.0),
        (-170.0, 65.0),
        (-114.0, 65.0),
        (-114.0, 0.0),
        (-170, 0.0)),
        srid=4326,
    )
    buoys = Buoy.objects.filter(point__within=poly)
    return [{'id': buoy.name, 'coords': buoy.point.coords}for buoy in buoys]