from mylog import *

def limit():
    # 2021-11-20 00:00 我是
    # pyinstaller.exe -F -p venv/Lib/site-packages/ booking.py
    if datetime.datetime.now() > datetime.datetime.strptime('2022-12-30 23:59', '%Y-%m-%d %H:%M'):
        logger.warning("试用期限已到...")
        return True
    return False
