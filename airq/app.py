# coding: utf-8

import os
import ipaddress
from collections import namedtuple

import requests
import geoip2.database
from geopy.geocoders import Nominatim
from flask import Flask, request, send_from_directory, jsonify as flask_jsonify

from .exceptions import AirqError

app = Flask(__name__)
app.config.update(dict(
    JSON_SORT_KEYS=False,
    GEOLITE=os.environ.get('GEOLITE'),
    FREEGEOIP_URL='https://freegeoip.net/json/',
    AQI_API_URL='https://api.waqi.info/feed/',
    AQI_API_TOKEN=os.environ.get('AQI_API_TOKEN', 'a80509ea0ada8c3d5a113999028b9e9b976a3f87')
))
app.debug = bool(os.environ.get('AIRQ_DEBUG'))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

geo_reader = geoip2.database.Reader(app.config['GEOLITE'])
geolocator = Nominatim()

pollutants = {
    'pm25': 'PM2.5',
    'pm10': 'PM10',
    'o3': 'O₃',
    'no2': 'NO₂',
    'so2': 'SO₂',
    'co': 'CO'
}


def jsonify(*args, **kwargs):
    response = flask_jsonify(*args, **kwargs)
    if not response.data.endswith(b'\n'):
        response.data += b'\n'
    return response


def get_ip(req):
    """Get ip address from http request.

    Attributes:
        req -- http request object
    """
    if req.headers.getlist("X-Forwarded-For"):
        ip = req.headers.getlist("X-Forwarded-For")[0]
        if ip.startswith('::ffff:'):
            ip = ip[7:]
    else:
        ip = req.remote_addr
    return ip


def get_location(ip):
    """Get geo location from ip address.

    Attributes:
        ip -- ip address
    """
    ip = ipaddress.ip_address(ip)
    app.logger.debug('{} is {}.'.format(ip, ip.is_private))
    if ip.is_private:
        # Get localhost's public IP.
        res = requests.get(app.config['FREEGEOIP_URL']).json()
        app.logger.debug(res)
        return namedtuple("Location", res.keys())(*res.values())  # make it looks like a geolocation object
    else:
        response = geo_reader.city(ip)
        return response.location


def get_air_quality(location):
    """Get air quality for location.

    Attributes:
        location -- geo location
    """
    if not (hasattr(location, 'latitude') and hasattr(location, 'longitude')):
        raise AirqError(404, "Sorry, cannot locate your location.")
    url = '{}geo:{};{}/'.format(app.config['AQI_API_URL'], location.latitude, location.longitude)
    app.logger.info(url)
    payload = {'token': app.config['AQI_API_TOKEN']}
    r = requests.get(url, params=payload).json()

    app.logger.info(r)
    if not r or r['status'] != 'ok':
        raise AirqError(404, "Sorry, something wrong happend.\n Please try again later.")

    for k, _ in pollutants.items():
        if k in r['data']['iaqi']:
            r['data'][k] = r['data']['iaqi'][k]['v']
    r['data']['station'] = r['data']['city']['name']
    time = r['data']['time']['s']
    del r['data']['time']
    r['data']['time'] = time
    del r['data']['attributions']
    del r['data']['city']
    del r['data']['iaqi']
    del r['data']['idx']
    return r['data']


@app.errorhandler(404)
def page_not_found(e):
    app.logger.error(e)
    return jsonify({'error': 'Not Found'}), 404


@app.errorhandler(AirqError)
def airq_error(e):
    app.logger.error(e)
    return jsonify({'error': e.message}), e.status_code


@app.errorhandler(500)
@app.errorhandler(Exception)
def internal_server_error(e):
    app.logger.error(e)
    return jsonify({'error': 'Server Error'}), 500


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def index():
    ip = get_ip(request)
    location = get_location(ip)
    app.logger.info(type(location))
    return jsonify(get_air_quality(location))


@app.route('/<string:location>')
def airq(location):
    location = geolocator.geocode(location)
    app.logger.info(location)
    return jsonify(get_air_quality(location))


if __name__ == '__main__':
    app.run()
