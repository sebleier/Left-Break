from django.conf.urls.defaults import *
from left_break.views import homepage


urlpatterns = patterns('',
    (r'^$', homepage),
)
