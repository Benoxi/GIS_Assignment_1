import flask
from flask import request, jsonify
from flask_cors import CORS

app = flask.Flask(__name__)
app.config["DEBUG"] = True
cors = CORS(app)

# http://164.8.252.95/geoserver/gis/wms?
# BBOX=346681.25,10081.25,633400,2114,>56.25&
# STYLES=&
# FORMAT=image/png&
# REQUEST=GetMap&
# VERSION=1.1.1&
# LAYERS=gis:P100004&
# WIDTH=800&
# HEIGHT=521&
# SRS=EPSG:2170

@app.route('/geoserver/gis/wms', methods=['GET'])
def wmsRequest():

    # Request validation
    for reqArgs in request.args:
        if len(request.args[reqArgs]) <= 0:
            return jsonify(reqArgs + " parameter is required!"), 422

    boundingBox = request.args['BBOX']
    styles = request.args['STYLES']
    format = request.args['FORMAT']
    req = request.args['REQUEST']
    version = request.args['VERSION']
    layers = request.args['LAYERS']
    width = request.args['WIDTH']
    height = request.args['HEIGHT']
    srs = request.args['SRS']

    print("\n")
    print(request)
    print("\n")

    return "Good request!"

app.run()
