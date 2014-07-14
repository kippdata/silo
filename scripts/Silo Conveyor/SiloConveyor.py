import argparse
import json
import csv
import zipfile
from datetime import datetime
from io import TextIOWrapper

from sqlalchemy import *

'''
Loads our configuration file, dwim.cfg, located in the same folder
'''
def load_config():
    
    try:
        f = open('***REMOVED***conv.cfg')
    except IOError as err:
        print('Problem opening ***REMOVED***conv.cfg!')
    else:
        with f:
            #Global variable config to be used in other parts
            global config

            config = json.load(f)

'''
Connects to our database to run neededs processes.
'''
def db_connect():

    #Start our sqlalchemy engine.
    global dwengine

    eng_conn_string = generate_db_url()
    
    dwengine = create_engine(eng_conn_string, echo=True)

    global dwconn

    dwconn = dwengine.connect()

'''
Generates the sqlalchemy database url, dependant on settings in dwim.cfg
'''
def generate_db_url():
    base = ''

    base += config['server-dialect']

    if config['server-driver'] != '':
        base += '+' + config['server-driver']

    base += '://'

    if config['server-username'] != '' and config['server-password'] != '':
        base += config['server-username'] + ':' + config['server-password']

    if config['server-host'] != '':
        base += '@' + config['server-host']

    if config['server-port'] != '':
        base += ':' + config['server-port']

    if config['server-database'] != '':
        base += '/' + config['server-database']

    return base

'''
Import the AssessmentResults.csv file into the map_table.
'''
def import_map(path):
    file_ext = path[-3:]
    if file_ext.lower() == 'zip':
        with zipfile.ZipFile(path) as mapzip:
            resultscsv = mapzip.open('AssessmentResults.csv')
            resultscsv = TextIOWrapper(resultscsv)
            results = list(csv.DictReader(resultscsv))
    elif file_ext.lower() != 'csv':
        print('Cannot handle %s file type. Zip or csv only.' % file_ext.lower())
        return
    else:
        with open(path) as file:
            results = list(csv.DictReader(file))

    check_map_table()

    results = convert_map_strings(results)

    dwconn.execute(map_table.insert(), results)    

'''
Checks that the map_table exists in the data warehouse.
If not, create it.
'''
def check_map_table():
    metadata = MetaData()

    global map_table

    map_table = Table('map_table', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('TermName', String(20)),
                      Column('StudentID', Integer()),
                      Column('SchoolName', String(50)),
                      Column('MeasurementScale', String(20)),
                      Column('Discipline', String(20)),
                      Column('GrowthMeasureYN', Boolean()),
                      Column('TestType', String(20)),
                      Column('TestName', String(50)),
                      Column('TestID', BigInteger()),
                      Column('TestStartDate', Date()),
                      Column('TestDurationMinutes', Integer()),
                      Column('TestRITScore', Integer()),
                      Column('TestStandardError', Float()),
                      Column('TestPercentile', Integer()),
                      Column('TypicalFallToFallGrowth', Integer()),
                      Column('TypicalSpringToSpringGrowth', Integer()),
                      Column('TypicalFallToSpringGrowth', Integer()),
                      Column('TypicalFallToWinterGrowth', Integer()),
                      Column('RITtoReadingScore', String(10)),
                      Column('RITtoReadingMin', String(10)),
                      Column('RITtoReadingMax', String(10)),
                      Column('Goal1Name', String(50)),
                      Column('Goal1RitScore', Integer()),
                      Column('Goal1StdErr', Float()),
                      Column('Goal1Range', String(10)),
                      Column('Goal2Adjective', String(10)),
                      Column('Goal2Name', String(50)),
                      Column('Goal2RitScore', Integer()),
                      Column('Goal2StdErr', Float()),
                      Column('Goal2Range', String(10)),
                      Column('Goal2Adjective', String(10)),
                      Column('Goal3Name', String(50)),
                      Column('Goal3RitScore', Integer()),
                      Column('Goal3StdErr', Float()),
                      Column('Goal3Range', String(10)),
                      Column('Goal3Adjective', String(10)),
                      Column('Goal4Name', String(50)),
                      Column('Goal4RitScore', Integer()),
                      Column('Goal4StdErr', Float()),
                      Column('Goal4Range', String(10)),
                      Column('Goal4Adjective', String(10)),
                      Column('Goal5Name', String(50)),
                      Column('Goal5RitScore', Integer()),
                      Column('Goal5StdErr', Float()),
                      Column('Goal5Range', String(10)),
                      Column('Goal5Adjective', String(10)),
                      Column('Goal6Name', String(50)),
                      Column('Goal6RitScore', Integer()),
                      Column('Goal6StdErr', Float()),
                      Column('Goal6Range', String(10)),
                      Column('Goal6Adjective', String(10)),
                      Column('Goal7Name', String(50)),
                      Column('Goal7RitScore', Integer()),
                      Column('Goal7StdErr', Float()),
                      Column('Goal7Range', String(10)),
                      Column('Goal7Adjective', String(10)),
                      Column('Goal8Name', String(50)),
                      Column('Goal8RitScore', Integer()),
                      Column('Goal8StdErr', Float()),
                      Column('Goal8Range', String(10)),
                      Column('Goal8Adjective', String(10)),
                      Column('TestStartTime', Time()),
                      Column('PercentCorrect', Integer()),
                      Column('ProjectedProficiency', String(20)))

    metadata.create_all(dwengine)
    
'''
Deals with the conversion of Strings from the csv into correct data types
'''
def convert_map_strings(results):
    for result in results:
        result['StudentID'] = convert_to_int(result['StudentID'])
        if result['GrowthMeasureYN'] == 'TRUE':
            result['GrowthMeasureYN'] = True
        else:
            result['GrowthMeasureYN'] = False
        result['TestID'] = convert_to_int(result['TestID'])
        result['TestStartDate'] = datetime.strptime(result['TestStartDate'],
                                                    '%m/%d/%Y').date()
        result['TestDurationMinutes'] = convert_to_int(
            result['TestDurationMinutes'])
        result['TestRITScore'] = convert_to_int(result['TestRITScore'])
        result['TestStandardError'] = convert_to_float(
            result['TestStandardError'])
        result['TestPercentile'] = convert_to_int(result['TestPercentile'])
        result['TypicalFallToFallGrowth'] = convert_to_int(
            result['TypicalFallToFallGrowth'])
        result['TypicalSpringToSpringGrowth'] = convert_to_int(
            result['TypicalSpringToSpringGrowth'])
        result['TypicalFallToSpringGrowth'] = convert_to_int(
            result['TypicalFallToSpringGrowth'])
        result['TypicalFallToWinterGrowth'] = convert_to_int(
            result['TypicalFallToWinterGrowth'])
        result['Goal1RitScore'] = convert_to_int(
            result['Goal1RitScore'])
        result['Goal1StdErr'] = convert_to_float(
            result['Goal1StdErr'])
        result['Goal2RitScore'] = convert_to_int(
            result['Goal2RitScore'])
        result['Goal2StdErr'] = convert_to_float(
            result['Goal2StdErr'])
        result['Goal3RitScore'] = convert_to_int(
            result['Goal3RitScore'])
        result['Goal3StdErr'] = convert_to_float(
            result['Goal3StdErr'])
        result['Goal4RitScore'] = convert_to_int(
            result['Goal4RitScore'])
        result['Goal4StdErr'] = convert_to_float(
            result['Goal4StdErr'])
        result['Goal5RitScore'] = convert_to_int(
            result['Goal5RitScore'])
        result['Goal5StdErr'] = convert_to_float(
            result['Goal5StdErr'])
        result['Goal6RitScore'] = convert_to_int(
            result['Goal6RitScore'])
        result['Goal6StdErr'] = convert_to_float(
            result['Goal6StdErr'])
        result['Goal7RitScore'] = convert_to_int(
            result['Goal7RitScore'])
        result['Goal7StdErr'] = convert_to_float(
            result['Goal7StdErr'])
        result['Goal8RitScore'] = convert_to_int(
            result['Goal8RitScore'])
        result['Goal8StdErr'] = convert_to_float(
            result['Goal8StdErr'])
        result['TestStartTime'] = datetime.strptime(result['TestStartTime'],
                                                    '%H:%M:%S').time()
        result['PercentCorrect'] = convert_to_int(
            result['PercentCorrect'])

    return results

'''
Converts a String to an integer. If blank returns None
'''
def convert_to_int(string):
    if string == '':
        return None
    else:
        return int(string)

'''
Converts a String to a float. If blank returns Non
'''
def convert_to_float(string):
    if string == '':
        return None
    else:
        return float(string)
    
#Commandline arguments setup
desc = 'Manage the import of data into the data warehouse.'
parser = argparse.ArgumentParser(description=desc)

parser.add_argument('-m', '--map', help='import the MAP Comprehensive Data File')

args = parser.parse_args()

#Start SQLAlchemy connection to data warehouse
load_config()
db_connect()

#Handle arguments
if args.map:
    try:
        import_map(args.map)
    except FileNotFoundError:
        print('File %s not found' % args.map)
