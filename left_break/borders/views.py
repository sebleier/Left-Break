from django.contrib.gis.geos import Point, Polygon
from django.views.decorators.cache import cache_page
from left_break.decorators import json_view
from left_break.borders.models import Coastline


#cache_page(60 * 15)
@json_view
def borders(request):
    boundaries = []
    borders = Coastline.objects.all()
    for border in borders:
        boundaries.append([(coord[0], coord[1]) for coord in border.geom.coords])
    return boundaries
