#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
import datetime

def mylog() :
    # logging.basicConfig()

    info_format = logging.Formatter('%(asctime)s - %(module)-6.6s [%(lineno)3.3d] : %(message)s')
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(info_format)
    console_handler.setLevel(logging.WARNING)
    console_handler.flush()

    file_handler = logging.FileHandler(filename="log-%s.txt"%(datetime.datetime.now().strftime('%Y%m%d-%H-%M-%S')),
                             mode='a',
                             encoding='utf-8',
                             delay=False)
    file_handler.setFormatter(info_format)
    file_handler.setLevel(logging.DEBUG)
    console_handler.flush()

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

logger = mylog()
