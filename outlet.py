import time
import coloredlogs
from tuyalinksdk.client import TuyaClient
from tuyalinksdk.console_qrcode import qrcode_generate
import json
from gpiozero import MotionSensor

from servo_motor import handleServo
from datetime import datetime

MANUAL_MODE = False
LAST_FED_TIME = None
LAST_MOTION_TIME = None

coloredlogs.install(level='DEBUG')

client = TuyaClient(productid='gsa0jbh7igkrxlq7',
                    uuid='tuyad5ab92434a30757f',
                    authkey='uRF4VSAk8BoWqP0Iexb1jvxBEQHjbheC')


def on_connected():
    print('Connected.')

def on_qrcode(url):
    qrcode_generate(url)

def on_reset(data):
    print('Reset:', data)

def on_dps(dps):
	global MANUAL_MODE
	global LAST_FED_TIME
	global LAST_MOTION_TIME

	print('DataPoints:', dps)
	if "101" in dps:
		if dps["101"] == True:
			handleServo("open")
			LAST_FED_TIME = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
			dps["102"] = LAST_FED_TIME
			client.push_dps(dps)
		elif dps["101"] == False:
			handleServo("close")
	if "103" in dps:
		MANUAL_MODE = dps["103"]


	if LAST_MOTION_TIME:
		dps["104"] = LAST_MOTION_TIME

	client.push_dps(dps)

client.on_connected = on_connected
client.on_qrcode = on_qrcode
client.on_reset = on_reset
client.on_dps = on_dps

client.connect()
client.loop_start()

pir = MotionSensor(26)

def movementDetected():
	global MANUAL_MODE
	global LAST_MOTION_TIME
	if MANUAL_MODE==True:
		handleServo("open")
		time.sleep(2)
		handleServo("close")
		LAST_MOTION_TIME = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

while True:
    # time.sleep(1)
    pir.wait_for_motion()
    print("Movement detected")
    LAST_MOTION_TIME = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    movementDetected()
    pir.wait_for_no_motion()
