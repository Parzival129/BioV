# Standard library imports
import sys
from time import sleep

# Third party imports
import serial
import DB.hashDB as hashDB

# Adafruit package imports
from adafruit_fingerprint import AdafruitFingerprint
from adafruit_fingerprint.responses import *

# # Example module imports
from fingerRecogEnroll import enroll_to_upper_computer

def getTemplate(hashedUsername):
    template = hashDB.getFinger(hashedUsername)
    return template

def storeTemplate(template:str, id: int=1):
    # Attempt to connect to serial port
    try:
        port = '/dev/ttyUSB0'  # USB TTL converter port
        baud_rate = '57600'
        serial_port = serial.Serial(port, baud_rate)
    except Exception as e:
        print(e)
        sys.exit()

    # Initialize sensor library with serial port connection
    finger = AdafruitFingerprint(port=serial_port)

    response = finger.vfy_pwd()
    if response is not FINGERPRINT_PASSWORD_OK:
        print('Did not find fingerprint sensor :(')
        sys.exit()
    print('Found Fingerprint Sensor!\n')

    if template:
        print(f'Template:: {template}')
        print(f'Storing template to flash library, with id #{id}\n')
        if store_from_upper_computer(finger=finger, template=template, page_id=id):
            print('Finished storing\n')
            return True
    else:
        print('Failed to return template')
        return False



def store_from_upper_computer(finger, template, page_id):
    # Buffer constants
    CHAR_BUFF_1 = 0x01
    CHAR_BUFF_2 = 0x02

    response = finger.down_char(buffer=CHAR_BUFF_1, template=template)
    if response is FINGERPRINT_OK:
        print('Template downloaded successfully!')
        sys.stdout.flush()
    if response is FINGERPRINT_PACKETRECEIVER:
        print('Communication error')
        return False
    if response is FINGERPRINT_TEMPLATEDOWNLOADFAIL:
        print('Template download error')
        return False

    response = finger.store(buffer=CHAR_BUFF_1, page_id=page_id)
    if response is FINGERPRINT_OK:
        print('Template stored successfully!')
        sys.stdout.flush()
        return page_id
    if response is FINGERPRINT_PACKETRECEIVER:
        print('Communication error')
        return False
    if response is FINGERPRINT_BADLOCATION:
        print('Could not store in that location')
        return False
    if response is FINGERPRINT_FLASHER:
        print('Error writing to flash')
        return False
