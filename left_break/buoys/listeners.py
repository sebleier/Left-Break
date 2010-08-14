from django.db.models.signals import post_syncdb
from left_break.buoys.load import load_buoy_data


def start_listening():
    import left_break.buoys.models
    post_syncdb.connect(load_buoy_data, sender=left_break.buoys.models)