import json
import datetime

def get_config(filename) :
    with open(filename, 'r') as thefile:
        return json.load(thefile)


def save(name, message):
    fo = open(name + '-' + datetime.datetime.now().strftime('%Y%m%d-%H-%M-%S') + '.txt', "w")
    fo.write(message)
    fo.close()