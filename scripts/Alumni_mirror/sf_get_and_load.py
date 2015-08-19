__author__ = 'Chris Haid'

## Imports
import databaseconfig
from config import SF_UID, SF_PWD, SF_TOKEN

from simple_salesforce import Salesforce
from pandas import DataFrame
from collections import defaultdict

## create database engine and open a connection
engine = databaseconfig.DB_ENGINE
conn = engine.connect()

## create a salesforce session
sf = Salesforce(username=SF_UID,
                password=SF_PWD,
                security_token=SF_TOKEN,
                organizationId='00Di0000000hSDR')

ktc_tables = sf.describe()
ktc_tables = ktc_tables[u'sobjects']
table_names = []

for i in ktc_tables:
    table_names.append(i[u'name'])

#the ones we want
desired_tables = ['Account', 'Contact', 'College_Persistence__c', 'Contact', 'Contact_Note__c', 'Enrollment__c']

all_tables = defaultdict()
for i in desired_tables:
    print 'Retrieving fields for table %s from Salesforce.' % i
    #this gets us the attributes of the table
    this_table = sf.__getattr__(i).describe()

    #this has the list of ordered dictionaries that describe the fields
    table_fields = this_table['fields']

    #list comprehension style
    field_names = []
    [field_names.append(item['name']) for item in table_fields]
    all_tables[i] = field_names

    # #non list comprehension style, fro reference

    # field_names = []
    # for item in table_fields:
    #     field_names.append(item['name'])

for i in all_tables:
    this_fields = all_tables[i]
    sql = "SELECT " + ",".join(this_fields) + " FROM " + i
    print "Getting table %s from Salesforce DB." % i
    sf_result = sf.query_all(sql)
    sf_df = DataFrame.from_dict(sf_result['records'], orient='columns', dtype=float)
    # drop attributes column if it exists, if not then pass
    try:
        sf_df.drop('attributes', axis = 1, inplace = True)
    except:
        pass
    # load table to database
    print "loading table %s into Silo." % i
    databaseconfig.create_sf_table(engine=engine, conn=conn, tablename= i, df=sf_df)

print "Done!"
