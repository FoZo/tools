#!/usr/bin/python

"""List all users and their grants in MySQL"""

import sys
import os.path
import ConfigParser
import pymysql
import argparse

"""Arguments part"""
parser = argparse.ArgumentParser(description="List all users and their grants in MySQL", usage="%(prog)s -u User -p Password -H Hostname -P Port")
parser.add_argument('-u', '--username', default="root", type=str, help='Default is root', metavar='User Name')
parser.add_argument('-p', '--password', type=str, help='Password', metavar='Password')
parser.add_argument('-H', '--host', default="localhost", type=str, help='Default is localhost', metavar='Hostname')
parser.add_argument('-P', '--port', default="3306", type=int, help='Default is 3306', metavar='Port Number' )
args = parser.parse_args()

""" Check username and password part """
home = os.path.expanduser("~")
mysql_username = args.username
mysql_password = args.password

if (not args.password) and (os.path.exists(home + '/.my.cnf')):
    if 'password' in open(home + '/.my.cnf').read():

        mysql_config = ConfigParser.RawConfigParser()
        mysql_config.read(home + '/.my.cnf')
        mysql_password = mysql_config.get('client','password')
        
        if 'user' in open(home + '/.my.cnf').read():
            mysql_username = mysql_config.get('client','user') 
        
        print ("Username is: " + mysql_username + "\nPassword is: " + mysql_password)

    else:
        print("\nError: Password is empty and there is no password in ~/.my.cnf \n")
        parser.print_help()
        sys.exit()


""" MySQL part"""
conn = pymysql.connect(host=args.host, user=mysql_username, passwd=mysql_password, port=args.port, db='mysql')
selusers = conn.cursor()
selgrants = conn.cursor()
selusers.execute("SELECT User,Host FROM user")
for response in selusers:
    print(response);
    print("SHOW GRANTS FOR \'" + response[0] + "\'@\'" + response[1] + "\'");

    selgrants.execute("SHOW GRANTS FOR \'" + response[0] + "\'@\'" + response[1] + "\'");
    
    for grants in selgrants:
        print(grants);
   
    print("\n");

selgrants.close()
selusers.close()
conn.close()
