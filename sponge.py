#!/usr/bin/env python

from datetime import datetime
from sys import argv
from flask import Flask, render_template, request, url_for


class Params(dict):
    def __setattr__(self, attr, value):
        self[attr] = value


app = Flask(__name__)

@app.route('/')
def index():
    v = Params()
    e = request.environ
    v.fields = str(e.keys())
    sn  = e["SCRIPT_NAME"]
    v.script_name = repr(sn)
    v.url_before = url_for("index")
    e["SCRIPT_NAME"] = "/sponge/"
    v.url_after = url_for("index")
    e["SCRIPT_NAME"] = sn
    v.path_info = repr(e["PATH_INFO"])
    return render_template('index.html', **v)

@app.route('/the-time')
def the_time():
    cur_time = str(datetime.now())
    return cur_time + ' is the current time!  ...YEAH!'

@app.route('/download/<filename>')
def download(filename):
    response = app.send_static_file(filename)
    response.headers["Content-type"] = "application/octet-stream"
    response.headers["Content-Disposition"] = "attachment;filename=" + filename
    return response

    
if __name__ == '__main__':
    opts = {}
    for arg in argv[1:]:
        if arg == "--public":
            opts["host"] = "0.0.0.0"
        if arg == "--debug":
            opts["debug"] = True
    else:
        app.run(**opts)
