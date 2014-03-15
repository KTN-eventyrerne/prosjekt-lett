#from client import Client
import socket
import threading
import json


def recieve():
    while(exit == False):
        try:
            jmsg = json.loads(connection.recv(1024))
            print jmsg[0].get('username') + ": " + jmsg[0].get('message')
        except:
            pass


print 'Hello and welcome to this chatting applciation'

host = 'localhost'
port = 9999

#fix connection
connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect((host, port))



#fix threads
exit = False
ko = []
lock = threading.Lock()

thread = threading.Thread(target = recieve)
thread.setDaemon(True)


loggedin = False
#do login sequence
while(not loggedin):
    username = raw_input('Select a user name: ')
    connection.send(json.dumps([{"request": "login", "username": username}]))
    status = json.loads(connection.recv(1024))
    
    if(status[0].get('error', '') == ''):
        loggedin = True

print "You are logged in"

thread.start()

#poll for msgs

while(exit == False):
    msg = raw_input('')
    if(msg == '/logout'):
        exit = True
        connection.send(json.dumps([{'request': 'logout'}]))
        #send logout msg and tear down connection
    else:
        #lock.acquire()
        connection.send(json.dumps([{"request": "message", "message": msg}]))
        #lock.release()

