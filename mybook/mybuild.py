import os
import myfile
import json

ret, accounts = myfile.get_config("account.json")
if ret == False :
    exit(0)

print(json.dumps(accounts))

for i in range(accounts) :

    os.system(r'pyinstaller.exe -F -p venv/Lib/site-packages/ mybook.py' + str(i))
