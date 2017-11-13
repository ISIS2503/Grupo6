import json
import requests
from requests.auth import HTTPBasicAuth

user = 'publisher'
passw = 'colmines12545'

url = "http://localhost:8000/mediciones"
payload={
    "user":user,
    "pw":passw,
    "idMicro": 1,
	"idSensor0": 2,
	"idSensor1": 3,
	"idSensor2": 4,
	"idSensor3": 5,
    "temperatura":23,
    "sonido":5,
    "gas":30,
    "luz":20,
    "time": 924812039
}
response = requests.post(url, data=json.dumps(payload), headers={'Content-type': 'application/json'}, auth=HTTPBasicAuth('publisher','colmines12545'))

print(str(response.status_code))
