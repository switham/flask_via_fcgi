#!/home/switham/.virtualenvs/feyzi/bin/python

from flup.server.fcgi import WSGIServer
from sponge import app as application

WSGIServer(application).run()
