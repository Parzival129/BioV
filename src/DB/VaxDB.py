"""
Has all the functions neccecary for interacting with the vaccination status database
"""

import boto3

s3_client = boto3.client('dynamodb')
DB = boto3.resource('dynamodb')
table = DB.Table('vaccination-statuses')

def getVaccinations(BioKey: str):
    '''
    gets the list of vaccinations for a specific biokey
    Ival: BioKey: str
    Rval: str
    '''
    response = table.get_item(
        Key = {'BioKey':BioKey}
    )
    return f"{response['Item']['Vaccinations']}"

def checkVaccination(BioKey: str, Vaccination: str) -> bool:
    '''
    checks the list of vaccinations for a user for a
    specific vaccinatoin
    Ival: BioKey: str
    Ival: Vaccination: str
    Rval: str
    '''
    vaccinations = getVaccinations(BioKey)
    res = bool(Vaccination in vaccinations)
    return res

def deleteItem(BioKey: str):
    '''
    Deletes all the information of a person in the database for a specific biokey
    Ival: BioKey: str
    Rval: int
    '''
    response = table.delete_item(Key = {'BioKey':BioKey})
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        response = table.delete_item(Key = {'BioKey':BioKey})
        return response["ResponseMetadata"]["HTTPStatusCode"]
    return 1

def registerVaccinations(BioKey: str, Vaccinations: str):
    '''
    registers vaccinations for someone
    Ival: BioKey: str
    Ival: Vaccinations: str
    Rval: int
    '''
    response = table.put_item(
        Item = {
            'BioKey':BioKey,
            'Vaccinations':Vaccinations
        }
    )
    return response["ResponseMetadata"]["HTTPStatusCode"]