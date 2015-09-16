"""
Python Script to pull CDF zip file from NWEA's MAP reporting site
    Need to authenticate to , then navigate to export page and save file with a an appropriate name
"""

print("Loading modules . . . ")
import requests
import cookielib
import shutil
import os
#from zipfile import ZipFile
from StringIO import StringIO
import zipfile
import pymssql
from datetime import datetime
import subprocess
import sys
import getopt
import ConfigParser as cp

print('Getting NWEA login credentials . . . ')

config = cp.ConfigParser()

config.read('get_MAP_CDF.config')

config.sections()

username = config.get('NWEA', 'username')
password = config.get('NWEA', 'password')
nwea_url = config.get('NWEA', 'url')

print("Retriving CDF . . . ")


r = requests.get(nwea_url, auth=(username, password))

print r.status_code, r.reason
if r.status_code == 200:
    print 'Downloading CDF...'
    ## convert the response content into a zipfile
    z = zipfile.ZipFile(StringIO(r.content))
    zfiles = z.namelist()


# Figure out year and season
def getSeasonYear():
    m =  datetime.now().month
    y = datetime.now().year
    y_string = datetime.now().strftime('%y')
    f_range = range(8,11)
    w_range = range(1,3) + [12]
    if m in range(8,11):
        return "Fall" + y_string
    elif m==12:	
	    y=y+1
	    y_string = str(y)[2] + str(y)[3]
	    return "Winter" + y_string
    elif m in range(1,3):
        return "Winter" + y_string
    else:
        return "Spring" + y_string

def getOptions(argv):
    if len(sys.argv)<2:
	    return # Return if no arguments passed
    inputdir = ''
    sy = ''
    try:
	    opts, args = getopt.getopt(argv, "s:i:")
    except:
	    print 'getMAP_CDF.py -s <season-year>'
	    sys.exit(2)
    for opt, arg in opts:
	    if opt in ('-s', '--season'):
		    sy = arg
	    elif opt in ('-i', '--inputdir'):
		    inputdir = arg
    print 'Season-year is: ',  sy
    print 'Input directory is: ', inputdir 
    return [sy,inputdir]

opts =  getOptions(sys.argv[1:])	
if len(sys.argv)>1:
    sy = opts[0]
    print "sy =", sy, " which has length ", len(sy)
elif len(sys.argv)==1:
    sy = getSeasonYear()


#Now to save the file
#get establish destination  directory
print("Unzipping CDF archive file . . . ")
dest_dir=os.getcwd()+'\\data\\'

# Test if season directory 
if not os.path.isdir(dest_dir):
    os.makedirs(dest_dir)


# Move and rename file in one line
z.extractall(dest_dir)

# Connect to Silo
print("Reading Silo credentials . . . ")

uid = config.get('Silo', 'uid')
pwd = config.get('Silo', 'pwd')
srvr = config.get('Silo', 'server')
prt = config.get('Silo', 'port')

print("Connetion to Silo data warehouse . . . ")
conn = pymssql.connect(server=srvr,
                           user=uid,
                           password=pwd,
                           port=prt)

cursor = conn.cursor()

print("Selecting NWEA database")
cursor.execute("USE [NWEA]")
print("Executing stored procedure to load CDF data . . .")
cursor.execute("exec msdb.dbo.sp_start_job N'NWEA | Refresh_CDF'")
conn.commit()

print("Closing connection . . .")
conn.close()

print("Done!")
# 5. Clean_up files