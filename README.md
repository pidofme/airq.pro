# airq.pro — check the air quality like a pro.

airq.pro is an air quality API service.

Check it at [airq.pro](http://airq.pro)

## Usage

You can access the service from a shell or from a Web browser:

```shell
$ curl airq.pro
{
  "aqi": 170, 
  "dominentpol": "pm25", 
  "pm25": 170, 
  "pm10": 83, 
  "o3": 23.2, 
  "no2": 29.3, 
  "so2": 8.2, 
  "co": 7.1, 
  "station": "People's Park, Chengdu", 
  "time": "2018-03-24 17:00:00"
}
```

You can specify a location, if you omit the location name,
you will get the report for your current location, based on your IP address.

```shell
$ curl airq.pro/Beijing
```

## Acknowledgements

* This service use [World Air Quality Index](http://aqicn.org) as data source for air quality information.

* This service includes GeoLite2 data created by MaxMind, available from [maxmind.com](http://maxmind.com). 