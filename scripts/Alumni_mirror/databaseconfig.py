__author__ = 'Charlie Bini'

import sqlalchemy as sa

from config import DB_TYPE, DB_API, DB_DNS_NAME, DB_NAME

## create database engine and open a connection
DB_CONN_STRING =  '%s+%s://%s'  % (DB_TYPE, DB_API, DB_DNS_NAME)
DB_ENGINE = sa.create_engine(DB_CONN_STRING)

def truncate_table(conn, tablename):
    """
    For truncating the destination table before loading in the new data
    Takes a SQLalchemy Connection object and the name of the SQL table to TRUNCATE
    """
    sql = """
        IF OBJECT_ID(N'%s') IS NOT NULL
            BEGIN
                TRUNCATE TABLE %s
            END
    """ % (tablename, tablename)
    trans = conn.begin()
    try:
        conn.execute(sql)
        trans.commit()
    except:
        trans.rollback()

def distress_signal(error_type, conn, body=''):
    trans = conn.begin()
    if error_type == 'traceback':
        warn_email = """
            DECLARE @body NVARCHAR(MAX);
            SET @body = '%s';
            EXEC msdb..sp_send_dbmail
                @profile_name = 'DataRobot',
                @recipients = 'cbini@teamschools.org',
                @body = @body,
                @subject = '!!! WARNING - GDocs Traceback !!!',
                @importance = 'High';""" % (body)
        conn.execute(warn_email)
        trans.commit()
    elif error_type == 'load':
        warn_email = """
            DECLARE @body NVARCHAR(MAX);
            SET @body = '%s';
            EXEC msdb..sp_send_dbmail
                @profile_name = 'DataRobot',
                @recipients = 'cbini@teamschools.org',
                @body = @body,
                @subject = '!!! WARNING - GDocs sp_LoadFolder Fail !!!',
                @importance = 'High';
        """ % (body)
        conn.execute(warn_email)
        trans.commit()


def create_sf_table(engine, conn, tablename, df):
    """
    Create or truncate and reload pandas df to RDBMS
    """
    try:
        # try to create table, but fail if it exists
        df.to_sql(tablename, engine, if_exists='fail')
    except:
        # truncate existing table
        truncate_table(conn, tablename)
        # "append" to the truncated destination table
        df.to_sql(tablename, engine, if_exists='append')
