import json
import requests
from datetime import datetime
import time
import googlemaps
import cgi
import os
import urllib
import pyipinfodb

def getWeather(coordsTuple):
	appid = "c7b29c1969be6fc524a538960a95f077"
	lat = str(coordsTuple[0])
	lon = str(coordsTuple[1])
	resp = requests.get("http://api.openweathermap.org/data/2.5/" \
	"weather?&lat="+lat+"&lon="+lon+"&units=imperial&APPID=" + appid)
	
	raw_dict = resp.json()
	temp = raw_dict.get('main').get('temp')
	city = raw_dict.get('name')
	country = raw_dict.get('sys').get('country')
	
	
	returnStr = ['The temperature in', city, country, 'is', \
	str(temp), 'degrees F']
	returnStr = ' '.join(returnStr)
	returnStr = str(returnStr)

	return returnStr

def getTime(coordsTuple):
	
	appid = 'AIzaSyCpf5jABcKAMKfmCWXqcNAbRZrSiTCLAu4'
	maps = googlemaps.Client(key=appid)	
	utc = time.time()
	lat = str(coordsTuple[0])
	lon = str(coordsTuple[1])
	time_resp = maps.timezone(lat+','+lon)
	dst_offset = time_resp.get('dstOffset') 
	raw_offset = time_resp.get('rawOffset')	
	current_time = (utc) + (dst_offset) + (raw_offset)
	current_time = datetime.fromtimestamp(current_time)
	return current_time.strftime('%b %d, %Y\t%I:%M')
	#return utc + dst_offset + raw_offset
	#return current_time

def getIP(environ):
	try:
		return environ['HTTP_X_FORWARDED_FOR'].split(',')[-1].strip()
	except KeyError:
		return environ['REMOTE_ADDR']	



def getCoords(IP):
	apiKey = '760e616ed6824e910cba5105edd16203e4d20' \
	'c52d759067395aec721a86cacac'
	ip_lookup = pyipinfodb.IPInfo(apiKey)
	resp = ip_lookup.get_city(IP)
	lat = resp['latitude']
	lon = resp['longitude']
	return (lat, lon)
	
	
def application(environ, start_response):
	start_response('200 OK', [('Content-Type','text/html')])
	return "<title> Super Sweet Python </title> \n" \
	"<h1><center>", getWeather(getCoords(getIP(environ))), " </h1> \n" \
	"<h2><center>", getTime(getCoords(getIP(environ))), "</h2>" 


