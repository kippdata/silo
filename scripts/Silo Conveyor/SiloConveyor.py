import sys
import argparse
import json
import csv
import zipfile
from datetime import datetime
from io import TextIOWrapper
from sqlalchemy import *


def load_config():
    """
    Loads our configuration file, ***REMOVED***conv.cfg, located in the same folder
    """
    try:
        f = open('***REMOVED***conv.cfg')
    except IOError:
        print('Problem opening ***REMOVED***conv.cfg!')
        sys.exit()
    else:
        with f:
            #Global variable config to be used in other parts
            global config

            config = json.load(f)


def db_connect():
    """
    Connects to our data warehouse to run needed processes.
    """

    #Start our sqlalchemy engine.
    global dwengine

    eng_conn_string = generate_db_url()
    
    dwengine = create_engine(eng_conn_string, echo=False)

    global dwconn

    dwconn = dwengine.connect()

    global dwmeta

    dwmeta = MetaData()

    dwmeta.reflect(bind=dwengine)


def generate_db_url():
    """
    Generates the sqlalchemy database url, dependant on setting in ***REMOVED***conv.cfg
    :return:String of database url
    """
    base = ''

    base += config['server-config']['server-dialect']

    if config['server-config']['server-driver'] != '':
        base += '+' + config['server-config']['server-driver']

    base += '://'

    if config['server-config']['server-username'] != '' and config['server-config']['server-password'] != '':
        base += config['server-config']['server-username'] + ':' + config['server-config']['server-password']

    if config['server-config']['server-host'] != '':
        base += '@' + config['server-config']['server-host']

    if config['server-config']['server-port'] != '':
        base += ':' + config['server-config']['server-port']

    if config['server-config']['server-database'] != '':
        base += '/' + config['server-config']['server-database']

    return base


def import_map(path):
    """
    Import the AssessmentResults.csv file into map_table.
    :param path: Path location of the file to import.
    """
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

    term = results[0]['TermName']

    dwconn.execute(map_table.delete().where(map_table.c.TermName == term))

    dwconn.execute(map_table.insert(), results)


def check_map_table():
    """
    Checks that the map_table exists in the data warehouse.
    If not, create it.
    """
    global map_table

    map_table = table_exists('map_table')

    if not map_table:

        map_table = Table('map_table', dwmeta,
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
                          Column('TypicalFallToFallGrowth', Float()),
                          Column('TypicalSpringToSpringGrowth', Float()),
                          Column('TypicalFallToSpringGrowth', Float()),
                          Column('TypicalFallToWinterGrowth', Float()),
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

        dwmeta.create_all(dwengine)


def convert_map_strings(results):
    """
    Handles conversion of csv Strings into correct data types
    :param results: The results from the csv read of the imported file
    :return:Returns corrected results list.
    """
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
        result['TypicalFallToFallGrowth'] = convert_to_float(
            result['TypicalFallToFallGrowth'])
        result['TypicalSpringToSpringGrowth'] = convert_to_float(
            result['TypicalSpringToSpringGrowth'])
        result['TypicalFallToSpringGrowth'] = convert_to_float(
            result['TypicalFallToSpringGrowth'])
        result['TypicalFallToWinterGrowth'] = convert_to_float(
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


def import_raw_powerschool():
    #psengine = create_engine('oracle://%s:%s@%s/PSPRODDB' %
    #                         (config['powerschool-config']['username'],
    #                          config['powerschool-config']['password'],
    #                          config['powerschool-config']['host']))

    #psmeta = MetaData()

    #students = Table('students', psmeta, autoload=True, autoload_with=psengine, schema='ps')

    pass

    #TODO Research and potentially implement Alembic module for raw data migration


def table_exists(table):
    """
    Check if a table already exists the the target data warehouse. If so return the table. Else return None.
    None to be used in if statements to see if table was loaded. For example:

    table = table_exists('table')
    if not table:
        #Generate table code

    :param table: Name of the table to check for
    :return:
    """
    if table in dwmeta.tables.keys():
        print('%s exists.' % table)
        return Table(table, dwmeta, autoload=True)
    else:
        print('%s does not exist.' % table)
        return None


def convert_to_int(string):
    """
    Converts a String to an integer. If blank returns None.
    :param string: String to convert.
    :return:None or int of String
    """
    if string == '':
        return None
    else:
        return int(string)


def convert_to_float(string):
    """
    Converts a String to a float. If blank returns None.
    :param string: String to convert.
    :return:None or float of String
    """
    if string == '':
        return None
    else:
        return float(string)
    
#Commandline arguments setup
desc = 'Manage the import of data into the KIPP Silo data warehouse.'
parser = argparse.ArgumentParser(description=desc)

parser.add_argument('-m', '--map', help='Import the MAP Comprehensive Data File')
parser.add_argument('-P', '--powerschoolraw', help='Import Raw PowerSchool tables', action='store_true')

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
        sys.exit()

if args.powerschoolraw:
    try:
        import_raw_powerschool()
    except Exception as e:
        print('Problem with Raw PowerSchool Import')
        print(e)
        sys.exit()