import pyodbc
import utilities.sqlserverport as db_access
servername = '10.10.20.22'
serverspec = '{0},{1}'.format(
    servername,
    db_access.lookup(servername, 'SQLEXPRESS'))
usrpwd = "I2FVGTestReader"
conn = pyodbc.connect('DRIVER=ODBC Driver 17 for SQL Server;SERVER={};UID={};PWD={}'.format(
    serverspec, usrpwd, usrpwd))