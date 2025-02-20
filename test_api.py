import json
import argparse
import requests
import sys


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-id", "--eventid", required=True,
	help="EventID from FrigateNVR")
ap.add_argument("-fip", "--frigate_ip", required=True,
	help="FrigateNVR IP")
ap.add_argument("-fp", "--frigate_port", required=True, default=5000,
	help="FrigateNVR TCP PORT")
ap.add_argument("-aip", "--api_ip", required=True,
	help="API IP")
ap.add_argument("-ap", "--api_port", required=True, default=8502,
	help="API TCP PORT")
ap.add_argument("-cu", "--cam_user", required=False, default="",
	help="CAM User")
ap.add_argument("-cp", "--cam_pass", required=False, default="",
	help="CAM Password")
ap.add_argument("-mu", "--mqtt_user", required=False, default="mqttuser",
	help="MQTT User")
ap.add_argument("-mp", "--mqtt_pass", required=False, default="mqttpass",
	help="MQTT Password")
ap.add_argument("-c", "--custom", required=False, default=False, type=lambda x: (str(x).lower() == 'true'),
	help="Enable Custom High Res URL")
ap.add_argument("-htl", "--h_to_l", required=False, default=False, type=lambda x: (str(x).lower() == 'true'),
	help="Froce High Res URL to Low Res URL")
args = vars(ap.parse_args())

event_id = args["eventid"]
FRIGATE_HOST = "http://" + args["frigate_ip"] + ":" + args["frigate_port"]
LNPR_API = "http://" + args["api_ip"] + ":" + args["api_port"] + "/alpr"
cam_user = args["cam_user"]
cam_pass = args["cam_pass"]
mqtt_user = args["mqtt_user"]
mqtt_pass = args["mqtt_pass"]
broker_address = args["frigate_ip"]

url_frigate_events = FRIGATE_HOST + "/api/events/" + event_id

ex_direct_cam_api = "http://" + args["frigate_ip"] + ":8123/local/frigate/snapshot/" + event_id + ".jpg"

r = requests.get(url_frigate_events)
try:
    json_r = r.json()
except json.JSONDecodeError as e:
    print("Can't Recheck Event ID\n")
    print("Invalid JSON syntax:", e)
    sys.exit()

camera = json_r["camera"]

l_url = FRIGATE_HOST + "/api/events/" + event_id + "/snapshot.jpg?bbox=0"
start_time = event_id.split("-")
start_time = start_time[0]
h_url = FRIGATE_HOST + "/api/" + camera + "/recordings/" + start_time + "/snapshot.png"
filename = event_id + ".jpg"

if args["custom"]:
    h_url = ex_direct_cam_api

if args["h_to_l"]:
    l_url = h_url

JSON_HEADERS = {
     "accept": "application/json",
     "Content-Type": "application/json; charset=utf-8"
}
payload = { "url": l_url,
            "h_url": h_url,
            "filename": filename,
            "cam_user": cam_user,
            "cam_pass": cam_pass,
            "url_frigate_events": url_frigate_events,
            "broker_address": broker_address,
            "mqtt_user": mqtt_user,
            "mqtt_pass": mqtt_pass
}

#print(payload)
r = requests.post(LNPR_API, headers = JSON_HEADERS, json = payload)
json_r = r.json()
print("Result : {}".format(json_r))
