"""
Has all the functions to register a users biokey in the biokey database
"""

import boto3
import cv2
from facialRecog2 import takephotos, faceRegistered, createModel
from fingerRecogEnroll import genTemplate
import os
import hashlib
import DB.hashDB as hashDB
from rich.console import Console
from datetime import datetime

BUCKET_NAME = 'bioauthfacedb2'
s3_client = boto3.client('s3')
console = Console()

def main():
    '''
    The main function that is initiated from the main.py file for registration
    Ival: None
    Rval: None
    '''
    print("Please enter your first and last name below (case sensitive)")
    firstName = input("First Name >> ")
    lastName = input("Last Name >> ")
    v = input("Do you have your covid-19 vaccinations? y/n >>")
    if v.lower().strip() == 'y':
        vaccinations = {'Covid-19'}
    else:
        vaccinations = {}
    username = (firstName + " " + lastName).encode()

    # choose hash function ur gonna use!
    # SHA-3: sha3_256
    # BLAKE2: blake2s

    hashedUsername = hashlib.blake2s(username).hexdigest()
    print("hashed username is: " + hashedUsername)
    registerFace(hashedUsername)
    print("")
    template = genTemplate()
    if template == False:
        return False
    date = datetime.now()
    print("Adding: " + hashedUsername, date.isoformat(), str(vaccinations) + " to DB")
    print("Returned with HTTP code: " + str(hashDB.registerBioKey(hashedUsername, template, date.isoformat(), vaccinations)))

def registerFace(hashedUsername) -> bool:
    '''
    Will add a face to the face DB
    Ival: str
    Rval: bool
    '''
    path = 'tempImageCache/new/person/temp.jpg'

    if faceRegistered(hashedUsername):
        console.print("[bold red]face with that name already exists in the face DB!")
        return False

    takephotos(path)
    createModel(hashedUsername)

    modelpath = f'tempImageCache/model/{hashedUsername}.clf'
    with open(modelpath, 'rb') as f:
        s3_client.upload_fileobj(f, BUCKET_NAME, hashedUsername)
    os.remove(modelpath)
    return True

def deleteFace(hashedUsername) -> bool:
    '''
    Will delete a face from the face DB
    Ival: str
    Rval" bool
    '''
    response = s3_client.delete_object(
    Bucket=BUCKET_NAME,
    Key=hashedUsername,
    )

    return True