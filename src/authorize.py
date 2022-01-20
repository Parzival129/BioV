"""
Has all the functions for authenticating a user based off of their biokey
"""

import boto3
import hashlib
import DB.VaxDB as VaxDB
from facialRecog2 import compare2
from fingerRecogStore import getTemplate, storeTemplate
from fingerRecog import checkFinger, empty
from rich.console import Console


BUCKET_NAME = 'bioauthfacedb2'
s3_client = boto3.client('s3')
console = Console()

def main():
    '''
    The main function that is initiated from the main.py file for authorization
    Ival: None
    Rval: None
    '''
    print("Please enter your first and last name below (case sensitive)")
    firstName = input("First Name >> ")
    lastName = input("Last Name >> ")
    VaccinationToCheck = input("Vaccination to authenticate >> ")
    name = (firstName + " " + lastName).encode()

    hashedUsername = hashlib.blake2s(name).hexdigest()


    
    if compare2(hashedUsername):
        console.print("[bold green]Facial biometric authorization complete!")
        storeTemplate(getTemplate(hashedUsername))
        if checkFinger():
            if VaxDB.checkVaccination(hashedUsername, VaccinationToCheck):
                console.print("[bold green]" + name.decode() + " has been vaccinated for " + VaccinationToCheck)
                console.print("[bold green]Welcome " + name.decode())
            else:
                console.print("[bold red]" + name.decode() + " has not been vaccinated for " + VaccinationToCheck)
            empty()
            return
    else:
        console.print("[bold red]Facial authorization failed!")
        empty()
        return
    empty()

def checkbiometrics():
    '''
    The other function that doesn't check vaccinations just the
    persons biometrics
    Ival: None
    Rval: None
    '''
    print("Please enter your first and last name below (case sensitive)")
    firstName = input("First Name >> ")
    lastName = input("Last Name >> ")
    name = (firstName + " " + lastName).encode()

    hashedUsername = hashlib.blake2s(name).hexdigest()
    if compare2(hashedUsername):
        console.print("[bold green]Facial biometric authorization complete!")
        console.print("[bold green]Welcome " + name.decode())
        return hashedUsername
    else:
        console.print("[bold red]Facial authorization failed!")
        return False