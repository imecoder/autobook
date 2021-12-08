# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
#
# import requests
#
# session = requests.session()
#
# session.get('http://www.qq.com')
# session.get('http://www.qq.com')


#!/usr/bin/env python
# -*- coding: UTF-8 -*

import time
import requests

import logging

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

s = requests.Session()
requests.get('http://www.qq.com')
requests.get('http://www.qq.com')
