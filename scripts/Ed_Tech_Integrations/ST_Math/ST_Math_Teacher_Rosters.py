"""ST_Math_Teacher_Roster
This script integrates PowerSchool with ST Math by pulling data down
from PowerSchool, create teachers.csv
and then pass those two files to ST Math vai SFTP
"""

# Import modules
print('Importing Python Modules')
import pandas as pd
import pymssql
import os
import pysftp
import ConfigParser as cp
from ST_Math_Rosters import convert_int

if __name__=='__main__':
# Connect to KIPP Silo
    print('Connecting to KIPP Silo')

    config = cp.ConfigParser()

    config.read('ST_Math.config')

    uid = config.get('Silo', 'uid')
    pwd = config.get('Silo', 'pwd')
    srvr = config.get('Silo', 'server')
    prt = config.get('Silo', 'port')


    conn = pymssql.connect(server=srvr,
                           user=uid,
                           password=pwd,
                           port=prt)


    # Construct teachers ps call
    print('Constructing SQL to pull teacher data from KIPP Silo')
    stmt = '''
            SELECT *
            FROM
            OPENQUERY(PS_CHI,'SELECT t.*
                                      FROM teachers t
                                      WHERE status=1
                                      AND homeschoolid!=0')
            '''

    # Excute Query
    print('Executing teachers query')
    teachers = pd.read_sql(stmt,conn)

    teachers.head(5)
    teachers.HOMESCHOOLID


    print('Assigning IIDs')
    teachers['iid'] = ""
    for numi, i in enumerate(teachers["SCHOOLID"]):
        if i == 78102:
            teachers["iid"][numi] = "KIP4OE"
        if i == 7810:
            teachers["iid"][numi] = "KIP4OH"
        if i == 400146:
            teachers["iid"][numi] = "KIP4OG"
        if i == 400163:
            teachers["iid"][numi] = "KIP4OF"

    print('Assigning school initials')
    teachers['school'] = ""
    for numi, i in enumerate(teachers["SCHOOLID"]):
        if i == 78102:
            teachers["school"][numi] = "KAP"
        if i == 7810:
            teachers["school"][numi] = "KAMS"
        if i == 400146:
            teachers["school"][numi] = "KCCP"
        if i == 400163:
            teachers["school"][numi] = "KBCP"



    print('Assigning positions and access levels')
    teachers['position'] = ""
    teachers['access_level'] = ""
    for numi, i in enumerate(teachers["PTACCESS"]):
        if i == 1:
            teachers["position"][numi] = 1
            teachers["access_level"] = 1
        if i == 0:
            teachers["position"][numi] = 8
            teachers["access_level"] = 3

    teachers.tail(10)

    print('Constructing students.csv')

    # teachers["email"] = ""

    # change column names


    teachers.head()
    teachers.columns.values


    teachers.rename(columns={'SCHOOLID' : 'district_school_id', 'TEACHERNUMBER' : 'district_teacher_id',
                            'LAST_NAME':'last_name', 'FIRST_NAME':'first_name',
                            'EMAIL_ADDR':'email'},
                   inplace=True)

    sel_cols = ['iid', 'district_school_id', 'school', 'district_teacher_id',
                'email','last_name','first_name', 'position', 'access_level']

    teachers_out = teachers[sel_cols]

    teachers_out = teachers_out.apply(convert_int)

    teachers_out.head(10)


    # get pwd
    path = os.getcwd()

    path = path + '\data'

    file_path = os.path.join(path,r'teachers.csv')


    print('Writing teachers.csv to ' + file_path)

    teachers_out.to_csv(file_path, index=False)

    print('Connectiong to ST Math SFTP service')

    host = config.get('STMathSFTP', 'host')
    password = config.get('STMathSFTP', 'password')
    username = config.get('STMathSFTP', 'username')

    with pysftp.Connection(host, username=username, password=password) as sftp:
        sftp.put(file_path)
        sftp.close()

    print 'Upload done.'




