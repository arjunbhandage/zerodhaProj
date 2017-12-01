import cherrypy
import os, os.path

class GainersAndLosers(object):
    @cherrypy.expose
    def index(self):
        return """<!DOCTYPE html>
<html>
<head>
<link href="./css/main.css" rel="stylesheet" type="text/css" />
</head>
<body >
	<h2 class="gainersLosersHeader">Top Gainers and Losers Nifty 50</h2>
	<div class="space">
	<div class="card">
		<img src="./images/img_avatar.png" alt="Avatar" style="width:10%">
		<div class="container">
			<h4><b>John Doe</b></h4> 
			<p>Architect & Engineer</p> 
		</div>
	</div>
	<div class="card">
		<img src="./images/img_avatar.png" alt="Avatar" style="width:10%">
		<div class="container">
			<h4><b>John Doe</b></h4> 
			<p>Architect & Engineer</p> 
		</div>
	</div>
</div>
</body>
</html> """

# On Startup
current_dir = os.path.dirname(os.path.abspath(__file__)) + os.path.sep
config = {
    'global': {
        'environment': 'production',
        'log.screen': True,
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 8080,
        'engine.autoreload_on': True
    },
    '/':{
        'tools.staticdir.root' : current_dir,
    },
    '/css':{
        'tools.staticdir.on' : True,
        'tools.staticdir.dir' : 'css',
    },
	'/images':{
        'tools.staticdir.on' : True,
        'tools.staticdir.dir' : 'images',
    },
}

if __name__ == '__main__':
    cherrypy.quickstart(GainersAndLosers(), '/', config)