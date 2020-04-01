#!/usr/bin/env python
# encoding: utf-8
"""
wait4db.py - Waits for a database to come up.  Used in docker entrypoints to ensure database container is started.


@author:     Aaron Kitzmiller
@copyright:  2019 The Presidents and Fellows of Harvard College. All rights reserved.
@license:    GPL v2.0
@contact:    aaron_kitzmiller@harvard.edu
"""
import os, sys
import time
import MySQLdb

APP_NAME = 'ifxtest'.upper()
SQL_DSN = {
    "host"      : os.environ.get("%s_HOSTNAME" % APP_NAME, "ifxtest"),
    "db"        : os.environ.get("%s_DATABASE" % APP_NAME, "ifxtest"),
    "user"      : os.environ.get("%s_USERNAME" % APP_NAME, "ifxtest"),
    "passwd"    : os.environ.get("%s_PASSWORD" % APP_NAME, "ifxtest"),
    "use_unicode" : True,
}

MAX_ATTEMPTS = int(os.environ.get("WAIT4DB_MAX_ATTEMPTS", 10))
SLEEPY_TIME = 2


def main():
    '''
    Keep attempting to connect to database until max attempts is reached.
    If max attempts is reached return 1, else return 0
    '''

    connection = None
    connection_attempts = 0
    while connection is None and connection_attempts < MAX_ATTEMPTS:
        try:
            connection = MySQLdb.connect(**SQL_DSN)
            return 0
        except Exception:
            time.sleep(SLEEPY_TIME)
            connection_attempts += 1
    return 1

if __name__ == '__main__':
    sys.exit(main())