import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib
import json
import pytz

# access to endpoint = http://localhost:8000/api?slack_name=Ezemba%20Marvellous&track=backend

HOST = 'localhost'
PORT = 8000

# Get the current day of the week
now = datetime.datetime.now(pytz.utc)
current_day = now.strftime("%A")
# print(current_day)

# Get current UTC time
current_time = now.strftime('%Y-%m-%dT%H:%M:%SZ')
# print(current_time)

# Data
data = {
    "slack_name": "Ezemba Marvellous",
    "current_day": current_day,
    "utc_time": current_time,
    "track": "backend",
    "github_file_url": "https://github.com/marviigrey/HNG-BACKEND-INTERNSHIP/blob/master/stage1/app.py",
    "github_repo_url": "https://github.com/marviigrey/HNG-BACKEND-INTERNSHIP",
    "status_code": 200
}

class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        
        parsed_url = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_url.query)

        slack_name = query_params.get('slack_name', [None])[0]
        track = query_params.get('track', [None])[0]

        if slack_name is not None and track is not None:
            data['slack_name'] = slack_name
            data['track'] = track

        # Convert the data dictionary to JSON format
        json_data = json.dumps(data)

        # Send the response headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        # Send the JSON data as the response body
        self.wfile.write(json_data.encode('utf-8'))


server = HTTPServer((HOST, PORT), RequestHandler)
print(f'Serving on port {PORT}')

# Server forever
server.serve_forever()
# close server
server.server_close()