"""
Run 'pytest tests.py' command to test the codebase with all the test functions
"""

from facialRecog2 import comparemodel2img
from DB.hashDB import getHTTP
from DB.VaxDB import checkVaccination

def test_compareimgs():
    '''checks the face for Russell Tabata'''
    assert comparemodel2img('testimgs/other2.jpeg', 'testimgs/59543c5ab76769d657137ad3dce03bb474d1987b9bf78c6e16ca0807f17a2936.clf', 'other2') == True

def test_compareimgs2():
    '''checks Thomas Lauder face against Russell Tabata to make sure no false positives'''
    assert comparemodel2img('testimgs/other1.jpeg', 'testimgs/test_model.clf', 'other1') == False

def test_user_db():
    '''checks hash DB for Russell Tabata'''
    assert getHTTP('59543c5ab76769d657137ad3dce03bb474d1987b9bf78c6e16ca0807f17a2936') == 200

def test_check_vaccinations():
    '''Checks that the vax DB is good'''
    assert checkVaccination('59543c5ab76769d657137ad3dce03bb474d1987b9bf78c6e16ca0807f17a2936', 'Covid-19') == True
    print("ALL CHECKS COMPLETED!")