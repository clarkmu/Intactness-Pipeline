"""Set up basic running parameters

Note: See configparser https://docs.python.org/3/library/configparser.html
"""

import os
import logging
import datetime
from configparser import ConfigParser, ExtendedInterpolation

# pylint: disable=C0103
# Invalid constant name
logger = logging.getLogger('pipe')


def configs(filename, seq_in):
    """Parse configurations
    """
    logger.info('Checking parameters')

    cfg = ConfigParser(interpolation=ExtendedInterpolation())

    cfg.read(filename)

    # ConfigParser.set resets .cfg variables
    if seq_in:
        seq_in_folder = seq_in[:seq_in.rindex('/')]
        cfg.set('Main', 'path_dat', seq_in_folder)
        cfg.set('Main', 'file_qry', seq_in)

    folder = cfg['Main']['path_out']
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Create a new log file each time the program is started
    date_tag = datetime.datetime.now().strftime("%Y-%b-%d_%H-%M-%S")
    file_log = "{}/run_{}.log".format(cfg['Main']['path_out'], date_tag)

    # Logging format: access time, logger name and message
    fmtr = logging.Formatter('%(asctime)s\t\t%(name)s\t\t%(message)s')

    fh = logging.FileHandler(file_log)
    fh.setLevel(logging.INFO)
    fh.setFormatter(fmtr)
    logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(fmtr)
    logger.addHandler(ch)

    return cfg
