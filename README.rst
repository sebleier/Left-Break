Install
=======

Assuming you have a fully functional Geodjango environment setup::

    createdb -T template_postgis left_break
    cd left_break
    ./manage.py syncdb --noinput
    ./manage.py load_buoys
    ./manage.py load_borders


