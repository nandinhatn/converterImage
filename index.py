def application(environ, start_response):
	status= '200 ok'
	html = '<html>\n'\
		'<body>\n'\
		'hello teste\n' \
		'</body>\n' \
		'</html>\n' 
	response_header = [('Content-type','text/html')]
	start_response(status,response_header)
	return [html]

