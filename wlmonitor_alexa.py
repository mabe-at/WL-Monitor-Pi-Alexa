#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, json, render_template
from flask_ask import Ask, request, session, question, statement, context, audio, current_stream

import sys, getopt
import json
import requests
import time
import unidecode
import re

apikey = False
apiurl = 'https://www.wienerlinien.at/ogd_realtime/monitor?rbl={rbl}&sender={apikey}'
rbls = []
flaskport = 5001

app = Flask(__name__)
ask = Ask(app, "/api")

def main(argv):
	global apikey
	global rbls
	global flaskport
	
	try:
		opts, args = getopt.getopt(argv, "hk:p:", ["help", "key=", "port="])
	except getopt.GetoptError: 
		usage()
		sys.exit(2)
	
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()                     
			sys.exit()                                    
		elif opt in ("-k", "--key"):
			apikey = arg
		elif opt in ("-p", "--port"):
			tmpport = int(arg)
			if tmpport > 0:
				flaskport = tmpport
	
	if apikey == False or len(args) < 1:
		usage()
		sys.exit()
	
	for rbl in args:
		rbls.append(rbl)

def usage():
	print 'usage: ' + __file__ + ' [-h] [-p port] -k apikey rbl [rbl ...]\n';
	print 'arguments:'
	print '  -k, --key=\tAPI key'
	print '  rbl\t\tRBL number\n'
	print 'optional arguments:'
	print '  -p, --port=\tPort to open (default 5001)'
	print '  -h, --help\tshow this help'

def gettimes():
	global apiurl
	global apikey
	global rbls
	
	texts = []
	rblquery = '&rbl='.join(rbls)
	url = apiurl.replace('{apikey}', apikey).replace('{rbl}', rblquery)
	#print url
	r = requests.get(url)
	if r.status_code == 200:
		try:
			for monitor in r.json()['data']['monitors']:
				station = nicestation(monitor['locationStop']['properties']['title'])
				for l in monitor['lines']:
					line = l['name']
					direction = nicestation(l['towards'])
					times = []
					iter = 2
					for d in l['departures']['departure']:
						if d['departureTime']['countdown'] > 1:
							times.append(d['departureTime']['countdown'])
							iter = iter -1
							if iter < 1:
								break
					
					if len(times) > 0:
						text = 'Linie {0} von {1}, in Richtung {2}, in {3}'.format(line, station, direction, times[0])
						
						if len(times) > 1:
							text = text + ' beziehungsweise {0}'.format(times[1])
						text = text + ' Minuten.'
						texts.append(text)
		except:
			texts = []
	
	if len(texts) > 0:
		return '\n'.join(texts)
	else:
		return False

def nicestation(station):
	station = re.sub(r"\sU$", "", station)
	station = re.sub(r",\s", " ", station)
	return station

@app.route('/')
def homepage():
	return 'Hallo! Das ist der Wiener-Linien-Monitor Alexa-Skill.'

@ask.launch
def start_skill():
	text = gettimes()
	if text:
		msg = 'Die nächsten Abfahrten sind:\n' + text
	else:
		msg = 'Ich habe keine Abfahrten gefunden.'
	#print msg	
	return statement(msg)


if __name__ == '__main__':
	main(sys.argv[1:])
	app.run(debug=True, port=flaskport)
