#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
import datetime

def mylog() :
    fmt = logging.Formatter('%(asctime)s - [%(lineno)3.3d] %(threadName)-10.10s: %(message)s')
    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    ch.setLevel(logging.INFO)
    ch.flush()
    fh = logging.FileHandler(filename="log-%s.txt"%(datetime.datetime.now().strftime('%Y%m%d-%H-%M-%S')), mode='a', encoding='utf-8')
    fh.setFormatter(fmt)
    fh.setLevel(logging.DEBUG)
    ch.flush()
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger

logger = mylog()
