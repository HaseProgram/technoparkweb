from cgi import parse_qsl

def application(env, start_response):
	output = b'<h2>Server response:</h2><br>'
	output += b'Hello world!<br><br>'
	requestParams = parse_qsl(env['QUERY_STRING'])
	if env['REQUEST_METHOD'] == 'GET':
		if env['QUERY_STRING'] != '':
			output += b'<b>GET data</b>:<br>'
			for data in requestParams:
				output += bytes(data[0], 'utf-8')
				output += b'='
				output += bytes(data[1], 'utf-8')
				output += b'<br>'

	if env['REQUEST_METHOD'] == 'POST':
		output += b'<b>POST data</b>:<br>'
		postParams = str(env['wsgi.input'].read(), 'utf-8').split('&')
		print(postParams)
		for data in postParams:
			output += bytes(data, 'utf-8')
			output += b'<br>'
	
	start_response('200 OK', [('Content-Type', 'text/html')])

	return iter([output])
