#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pprint
import logging

from utils import get_session_id
from config import pkg_structure, handlers, config

logger = logging.getLogger(__name__)

def parse(string):
    """
    This function receive raw string (package) in next format: 
        @ses_id;pkg_type;date;time;;...;;;#
    Parse this string and depending on package type call next function to parse
    left data fields.
    Args:
        string: String @;;;#
    Returns:
        Dictionary with parsed data and three fields named ses_id, type(package
        type), original (original string)
    """
    if not string:
        return string

    # Parse and convert data
    result = dict()

    # Add original string to dict. Later it will be used to it to file.
    result['original'] = string.rstrip()

    # Check if receive complete string
    if string[0] != config['pkg_start'] or string[-1] != config['pkg_end']:
        logger.error('Sorry, string is not complete. String: {}'.format(string))
        result['ses_id'] = 0
        result['type'] = 'E'
        return result
    
    # Get rid of package characters and split data into list
    raw_data = string[1:-1].split(config['pkg_delimeter'])
    # Remove empty positions
    data_list = list(filter(None, raw_data))

    # Setup some specific fields. This fields are common for all packages.
    try:
        result['ses_id'] = get_session_id(int(data_list.pop(0)))
        result['type'] = data_list.pop(0)
    except:
        # This is case if package really bad and hasn't some basic fields.
        logging.info('Fail to parse primary fields. Package is wrong.')
        result['ses_id'] = 0
        result['type'] = 'E'

    # Based on package type choose next parser.
    if result['type'] == 'I':
        pass
    elif result['type'] == 'T':
        result.update(parse_msg(data_list))
    elif result['type'] == 'D':
        result.update(parse_data(data_list))
    else:
        logging.info('Unknown package type. Just save it to file.')

    return result


def parse_msg(data_list):
    '''
    Parse message package. 
    '''
    result = dict()

    result['msg'] = str(';'.join(data_list[1:]))
    try:
        result['ses_time'] = handlers['time_ms_out'](data_list[0])
    except ValueError:
        logging.error('There is wrong data or handler. The sample skipped.')
        with open(config['corrupted_storage'], 'a+') as corrupted_storage:
            corrupted_storage.write(string + '\n')



    return result

def parse_data(data_list):
    '''
    This function receive string which represent data package sent by logger.
    Then this string is parsed into separate elements. Those data are added 
    to resulting dictionary.
    Args:
        str: package string in the next format: @;;;...;;;;#
    Returns:
        Dictionary with names and converted data.
    '''
    # Parse and convert data
    result = dict()

    for i, name in enumerate(pkg_structure):
        try:
            if data_list[i] != 'x':
                result[name] = handlers[name](data_list[i])
            else:
                result[name] = 'NULL'

        except ValueError:
            # We don't want to loose data in any case so we save it to file
            logging.error('There is wrong data or handler. The sample skipped.')
            result[name] = 'NULL'
        except TypeError:
            logging.error('Can\'t parse string. Possibly there is problem with '
                         ' some handler. Handler should be callable function.')
            result[name] = 'NULL'
        except IndexError:
            logging.error('There is IndexError, possibly package contains wrong'
                         ' number of field.')
            result[name] = 'NULL'

    return result

if __name__ == '__main__':
    test_list = [
        '@010;T;00:00:00;Var. init.;SW:PaPa,0.2;HW:s12,SIM5320e,bastl#',
        '@010;T;00:00:00;Reset#',
        '@010;T;00:00:05;Init wait done.#',
        '@010;T;00:00:05;Modem init done.#',
        '@010;D;13.08.16;10:24:49.0;5004.340927N;01432.673110E;6.2;323.4;298.61;8;1;319;99479#',
        '@010;D;x;x;x;x;x;x;x;x;x;320;99486#',
        '@010;D;x;x;x;x;x;x;x;x;x;320;99473#',
        '@010;D;x;#',
        '@010;D;13.08.16;10:24:49.0;5004.340927N;01432.673110E;6.2;323.4;298.61;8;1;319;99479#',
        '@010;D;13.08.16;10:24:53.0;5004.349060N;01432.666529E;9.1;336.7;299.41;8;1;-1;-1#',
        '@010;T;00:00:15;GSM Process error.#',
        '@asdfasdfasdfasdfadsf#'
    ]

    for line in test_list:
        pprint.pprint(parse(line))
