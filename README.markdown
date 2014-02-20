# news.loogica.net

TODO: add some description here. :-)

## Installation

Create a [virtualenv](virtualenv) for the project and activate it:

    virtualenv .env
    source .env/activate

Install dependencies:

    pip install -r requirements.txt

If you get the error `ImportError: No module named setuptools.command`, try
this out:

    wget http://python-distribute.org/distribute_setup.py
    python distribute_setup.py
    easy_install pip
    pip install -r requirements.txt

## Running

Please change `settings.ini` as needed and then, run:

    python web.py

[virtualenv]: https://pypi.python.org/pypi/virtualenv
