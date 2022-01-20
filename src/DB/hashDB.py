"""
Has all the functions for interacting with the BioKey user database
"""

import boto3
from DB.VaxDB import registerVaccinations

s3_client = boto3.client('dynamodb')
DB = boto3.resource('dynamodb')
table = DB.Table('BioKeys')
vaxtable = DB.Table('vaccination-statuses')
# Get functions
def getName(BioKey: str):
    '''
    gets the name from the database for a specific biokey
    Ival: BioKey: str
    Rval: str
    '''
    response = table.get_item(
        Key = {'BioKey':BioKey}
    )
    return f"{response['Item']['First Name']} {response['Item']['Last Name']}"

def getDate(BioKey: str):
    '''
    gets the registration date from the database for a specific biokey
    Ival: BioKey: str
    Rval: str
    '''
    response = table.get_item(
        Key = {'BioKey':BioKey}
    )
    return response['Item']['Registration Date']

def getFinger(BioKey: str):
    '''
    gets the registration date from the database for a specific biokey
    Ival: BioKey: str
    Rval: str
    '''
    response = table.get_item(
        Key = {'BioKey':BioKey}
    )
    return response['Item']['Template']

def getItem(BioKey: str):
    '''
    gets the total information from the database for a specific biokey
    Ival: BioKey: str
    Rval: str
    '''
    response = table.get_item(
        Key = {'BioKey':BioKey}
    )
    return response['Item']

def deleteItem(BioKey: str):
    '''
    Deletes all the information of a person in the database for a specific biokey
    Ival: BioKey: str
    Rval: int
    '''
    response = table.delete_item(Key = {'BioKey':BioKey})
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        response = vaxtable.delete_item(Key = {'BioKey':BioKey})
        return response["ResponseMetadata"]["HTTPStatusCode"]
    return 1
def getHTTP(BioKey: str):
    '''
    gets the http status code for a user
    Ival: BioKey: str
    Rval: int
    '''
    response = table.get_item(
        Key = {'BioKey':BioKey}
    )
    return response["ResponseMetadata"]["HTTPStatusCode"]

# Post Functions

def registerBioKey(BioKey, Template, Date, Vaccinations):
    '''
    puts the inputed data for a biokey and returns the HTTP status code for it
    Ival: BioKey: str
    Ival: Template: str
    Ival: Date: str
    Ival: Vaccinations: set
    Rval: str
    '''
    columns = ['Template', 'Registration Date']
    response = table.put_item(
        Item={
            'BioKey':BioKey,
            columns[0]:Template,
            columns[1]:Date,
        }
    )
    if registerVaccinations(BioKey, Vaccinations) != 200:
        print("an error occured registering to vaccination")
    return response["ResponseMetadata"]["HTTPStatusCode"]
