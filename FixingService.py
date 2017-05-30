#!/usr/bin/env python

import os
import sys
import getopt

from flask import Flask,make_response,Response,request,render_template

port=28083

app = Flask("FixingService", static_url_path='')

@app.route('/data/<ric>')
def loadFixing(ric=''):
	output=''

	with open('data/' + ric + '.csv', 'rb') as fd:
		output = fd.read()

	return Response(output, content_type='text/plain')

@app.route('/graph/<ric>')
def graph(ric=''):
	width=1000
	height=500

	if 'width' in request.values:
		width = int(request.values['width'])
	if 'height' in request.values:
		height= int(request.values['height'])

	return render_template('graph.html', ric=ric, width=width, height=height)

@app.route('/graph')
def graph_index():
	rics = [ f[:-4] for f in os.listdir('data') if f[-4:] == '.csv' ]
	return render_template('graph_index.html', rics=rics)

opts,args = getopt.getopt(sys.argv[1:], 'U:P:p:')

for opt,arg in opts:
	if opt == '-p':
		try:
			port = int(arg)
		except:
			print 'invalid port number: ' + arg
			exit(1)


app.run(host='0.0.0.0', port=port)


