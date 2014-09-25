"""ST_Math_Roster
This script integrates PowerSchool with ST Math by pulling data down
from KIPP Silo linked PowerSchool, creates two files (students.csv and teachers.csv)
and then pass those two files to ST Math vai SFTP.

You must fill in the fields in ST_Math.config to match your silo instance, 
any conditions on your students you need (grade levels, schools, etc.) using a Oracle SQL WHERE 
conditions (no need to quote) in the condition argument.  Leaving the argument blank will 
pull all of your currently enrolled students. 

You must also add your ST Math SFTP credentials in the STMathSFTP section.
"""
# Import modules
print('Importing Python Modules')
import pandas as pd
import pymssql
import os
import pysftp
import ConfigParser as cp


def convert_int(x):
    try:
        return x.astype(int)
    except:
        return x


if __name__ == "__main__":
    # Connect to KIPP Silo
    print('Connecting to KIPP Silo')

    config = cp.ConfigParser()

    config.read('ST_Math.config')

    uid = config.get('Silo', 'uid')
    pwd = config.get('Silo', 'pwd')
    srvr = config.get('Silo', 'server')
    prt = config.get('Silo', 'port')
    condn = config.get('Silo', 'condition')

    if condn!='':
        condn = 'AND ' + condn



    conn = pymssql.connect(server=srvr,
                           user=uid,
                           password=pwd,
                           port=prt)


    # Construct students ps call
    print('Constructing SQL to pull student data from KIPP Silo')
    stmt = '''
              SELECT *
              FROM
              OPENQUERY(PS_CHI,'SELECT  student_number,
                                        last_name,
                                        first_name,
                                        ps_customfields.getStudentscf(id,''student_email'') as student_email,
                                        ps_customfields.getStudentscf(id,''student_web_username'') as student_uid,
                                        ps_customfields.getStudentscf(id,''student_web_pwd'') as student_pwd,
                                        SchoolID,
                                        grade_level,
                                        home_room
                                        FROM students
                                        WHERE enroll_status=0
                                        %s')
              ''' % condn

    # Excute Query
    print('Executing students query')
    students = pd.read_sql(stmt,conn)

    students.head(100)



    # Construct teachers ps call
    print('Constructing SQL to pull teacher data from KIPP Silo')
    stmt = '''
              SELECT *
              FROM
              OPENQUERY(PS_CHI,'SELECT  First_Name, Last_Name, HomeSchoolId, TeacherNumber
                                        FROM teachers
                                        WHERE status=1')
              '''

    # Excute Query
    print('Executing students query')
    teachers = pd.read_sql(stmt,conn)

    teachers.head(5)



    print('Assigning IIDs')
    students['IID'] = ""
    for numi, i in enumerate(students["SCHOOLID"]):
        if i == 78102:
            students["IID"][numi] = "KIP4OE"
        if i == 7810:
            students["IID"][numi] = "KIP4OH"
        if i == 400146:
            students["IID"][numi] = "KIP4OG"
        if i == 400163:
            students["IID"][numi] = "KIP4OF"

    print('Assigning school initials')
    students['School'] = ""
    for numi, i in enumerate(students["SCHOOLID"]):
        if i == 78102:
            students["School"][numi] = "KAP"
        if i == 7810:
            students["School"][numi] = "KAMS"
        if i == 400146:
            students["School"][numi] = "KCCP"
        if i == 400163:
            students["School"][numi] = "KBCP"


    students.tail(10)


    # Consturct teachers P1 A ps call
    print('Constructing SQL to pull first period teacher data from KIPP Silo')
    stmt = '''
          SELECT *
          FROM
          OPENQUERY(PS_CHI,'SELECT  st.*,
                                    t.teachernumber,
                                    s.student_number
                            FROM		(
                                    SELECT  studentid,
                                            teacherid,
                                            expression
                                    FROM    cc
                                    WHERE   expression=''1(A)''
                                    AND     termid=2400
                                    ) st
                            JOIN teachers t
                            ON st.teacherid=t.id
                            JOIN students s
                            ON st.studentid = s.id')
              '''

    # Excute Query
    print('Executing students query')
    P1A_teachers = pd.read_sql(stmt,conn)

    P1A_teachers.head(5)


    print('Closing connection to KIPP Silo')
    conn.close()

    # join P1(A) Teachers to students
    print('Joining Period 1 teachers (i.e., home room teachers) to students')
    students_P1A = students.merge(P1A_teachers, on='STUDENT_NUMBER', how='left')

    students_P1A.head(10)
    # join teacher data to studetns and period 1 teacher information
    print('Joining other teacher data to student file')

    student_teacher = students_P1A.merge(teachers, on='TEACHERNUMBER', how='left')

    student_teacher.head(10)


    print('Constructing students.csv')

    student_teacher["teacher_email"] = ""
    student_teacher["curriculum"] = ""
    student_teacher["new_student_id"] = ""
    student_teacher["permanent_login"] = ""
    student_teacher["birth_date"] = ""
    student_teacher["action"] = ""
    student_teacher["period"] = ""


    student_teacher.columns=[x.lower() for x in student_teacher.columns]


    student_teacher.head()

    student_teacher.rename(columns={'schoolid': 'district_school_id', 'teachernumber': 'district_teacher_id',
                                    'last_name_y': 'teacher_last_name', 'first_name_y' : 'teacher_first_name',
                                    'grade_level' : 'grade', 'student_number' : 'student_id','last_name_x' : 'student_last_name',
                                    'first_name_x': 'student_first_name', 'student_uid': 'student_username', 'student_pwd' : 'student_password'},
                           inplace=True)

    student_teacher.head(5)

    select_cols = []
    select_cols = ["iid","district_school_id","school","district_teacher_id", "teacher_email"]
    select_cols.extend(["teacher_last_name", "teacher_first_name", "grade", "period", "curriculum"])
    select_cols.extend(["student_id", "new_student_id", "student_last_name", "student_first_name"])
    select_cols.extend(["student_username", "student_password", "permanent_login", "birth_date", "action"])
    select_cols

    student_teacher.head()

    student_out = student_teacher[select_cols]


    student_out.head(10)

    # Quick function to convert doubles to integers

    student_out = student_out.apply(convert_int)
    student_out.head(10)

    # get pwd
    path = os.getcwd()

    path = path + '\data'

    file_path = os.path.join(path,r'students.csv')


    print('Writing students.csv to ' + file_path)

    student_out.to_csv(file_path, index=False)

    print('Connectiong to ST Math SFTP service')


    host = config.get('STMathSFTP', 'host')
    password = config.get('STMathSFTP', 'password')
    username = config.get('STMathSFTP', 'username')

    with pysftp.Connection(host, username=username, password=password) as sftp:
        sftp.put(file_path)
        sftp.close()

    print 'Upload done.'




