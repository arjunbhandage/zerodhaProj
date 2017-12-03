import cherrypy
import os
import json
import requests
import redis
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('html'))
urlGainers = "https://www.nseindia.com/live_market/dynaContent/live_analysis/gainers/niftyGainers1.json"
urlLosers = "https://www.nseindia.com/live_market/dynaContent/live_analysis/losers/niftyLosers1.json"


class GainersAndLosers(object):

    @cherrypy.expose
    def index(self):
        r = redis.Redis(host="ec2-34-233-217-71.compute-1.amazonaws.com", port="43969", db=0, password="p7551f57171f509a98262374f76c4aa523dd3640f6db8312dbcbf0a886791397d")
      
        resp = requests.get(urlGainers)
        json_data_gainers = json.loads(resp.text)
        resp = requests.get(urlLosers)
        json_data_losers = json.loads(resp.text)
        r.hmset("topGainers", json_data_gainers)
        r.hmset("topLosers", json_data_losers)
        topLosers = r.hgetall("topLosers")
        topGainers = r.hgetall("topGainers")
        markup = """ <h4><b> Top Gainers </b></h4> """
          
        topGainers = topGainers['data'].replace("u'","\"")
        topGainers = topGainers.replace("'","\"")
        jsonTopGainers = json.loads(topGainers)
        for data in jsonTopGainers:
            #percentageChange = ((float(data["ltp"])-float(data["previousPrice"]))/float(data["previousPrice"]))*100
            markup += """ <div class="card">
            <img src="./assets/img_avatar.png" alt="Avatar" style="width:10%">
            <div class="container">
                <h4><b>Symbol: """+data["symbol"]+"""</b></h4>
                <p>LTP: """+data["ltp"]+"""</p> 
                <p>Open: """+data["openPrice"]+"""</p> 
                <p>High: """+data["highPrice"]+"""</p> 
                <p>Low: """+data["lowPrice"]+"""</b></p> 
                <p>Previous Price: """+data["previousPrice"]+"""</p>    
                <p>Traded Quantity: """+data["tradedQuantity"]+"""</p>
                <p>Turnover: """+data["turnoverInLakhs"]+""" Lakhs</p> 
                <p>"""+data["lastCorpAnnouncementDate"]+"""</p>
            </div>
            </div>"""
            
        topLosers = topLosers['data'].replace("u'","\"")
        topLosers = topLosers.replace("'","\"")
        jsonTopLosers = json.loads(topLosers)
        markup += """ <h4><b> Top Losers </b></h4> """
        for data in jsonTopLosers:
            #percentageChange = ((float(data["ltp"])-float(data["previousPrice"]))/float(data["previousPrice"]))*100
            markup += """ <div class="card">
            <img src="./assets/img_avatar.png" alt="Avatar" style="width:10%">
            <div class="container">
                <h4><b>Symbol: """+data["symbol"]+"""</b></h4>
                <p>LTP: """+data["ltp"]+"""</p> 
                <p>Open: """+data["openPrice"]+"""</p> 
                <p>High: """+data["highPrice"]+"""</p> 
                <p>Low: """+data["lowPrice"]+"""</b></p> 
                <p>Previous Price: """+data["previousPrice"]+"""</p>
                <p>Traded Quantity: """+data["tradedQuantity"]+"""</p>
                <p>Turnover: """+data["turnoverInLakhs"]+""" Lakhs</p> 
                <p>"""+data["lastCorpAnnouncementDate"]+"""</p>
            </div>
            </div>"""
        
        data_to_show = [markup]
        tmpl = env.get_template('index.html')
        return tmpl.render(data=data_to_show)

  
config = {
    'global': {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': int(os.environ.get('PORT', 5000)),
		#'server.socket_host': '127.0.0.1',
        #'server.socket_port': 8080,
    },
    '/assets': {
        'tools.staticdir.root': os.path.dirname(os.path.abspath(__file__)),
        'tools.staticdir.on': True,
        'tools.staticdir.dir': 'assets',
    }
}

cherrypy.quickstart(GainersAndLosers(), '/', config=config)
