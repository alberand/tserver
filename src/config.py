#!/bin/python

from datetime import datetime

config = {
        # MySQL information
        # Host is usually localhost, if database is running on another machine
        # it should be change to address of that machine.
        'mysql_host':   'localhost',
        # User name
        'mysql_user':   'cast',
        # Password
        'mysql_pass':   'castpass',
        # Name of the DATABASE (not a table)
        'mysql_db':  'loggersdb',

        # Socket parameters
        'host': 'localhost',
        'port': 5000
}

# This list define package structure. Thus, in which order data are arranged.
# Empty fields doesn't appear in data structure. They are just skipped, also as
# non defined fields.
pkg_structure = [
        'module_id',
        'date',
        'time',
        'latitude',
        'longitude',
        'course',
        'gps_altitude',
        'speed',
        'temperature',
        'pressure',
        'unknown_1',
        'unknown_2'
]

# This dictionary define data handlers. There is no need to keep right order.
# Handler should be pointer (object) to callable function not result of calling
# this function.
handlers = {
        # Name  # Handler
        'module_id':    int,
        'date':         lambda date: 
                                datetime.strptime(date, '%d.%m.%y').date(),
        'time':         lambda time: 
                                datetime.strptime(time, '%H:%M:%S.%f').time(),
        'latitude':     lambda data: [float(data[:-1]), str(data[-1])],
        'longitude':    lambda data: [float(data[:-1]), str(data[-1])],
        'course':       float,
        'gps_altitude': float,
        'speed':        float,
        'temperature':  int,
        'pressure':     int,
        'unknown_1':    int,
        'unknown_2':    int
}
