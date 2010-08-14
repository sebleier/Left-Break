from django.db.models.signals import post_syncdb
from left_break.borders.load import load_border_data


def start_listening():
    import left_break.borders.models
    post_syncdb.connect(load_border_data, sender=left_break.borders.models)