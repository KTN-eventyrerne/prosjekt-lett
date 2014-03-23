#from client import Client
import socket
import threading
import json

exit = False

def recieve():
    global logedin
    global exit
    while(exit == False):
        try:
            jmsg = json.loads(connection.recv(1024))
	    if jmsg[0].get('response') == "logout" and jmsg[0].get('error') == "Not logged in!":
		print "You are not logged in, unable to logout..."
		loggedin = False
	    if jmsg[0].get('response') == "logout" and jmsg[0].get('error') != "Not logged in!" and jmsg[0].get('username') != "":
		print "Logout sucsess!"
		exit = True
            print jmsg[0].get('username') + ": " + jmsg[0].get('message')
        except:
            pass


print 'Hello and welcome to this chatting applciation'

host = 'localhost'
port = 9997

#fix connection
connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect((host, port))



#fix threads
loggedin = False
exit = False
ko = []
lock = threading.Lock()

thread = threading.Thread(target = recieve)
thread.setDaemon(True)



#do login sequence
while(not loggedin):
    username = raw_input('Select a user name: ')
    connection.send(json.dumps([{"request": "login", "username": username}]))
    status = json.loads(connection.recv(1024))
    
    if(status[0].get('error', '') == ''):
        loggedin = True
    elif(status[0].get('error', '') == "Name already taken!"):
	print "Name already taken!"
    elif(status[0].get('error', '') == "Invalid username!"):
	print "Invalid username!"
	

print "You are logged in"


thread.start()

#poll for msgs

while(exit == False):
    msg = raw_input('')
    if(msg == "\logout"):
	print msg
        ##exit = True
        connection.send(json.dumps([{'request': 'logout'}]))
        #send logout msg and tear down connection
    else:
        #lock.acquire()
        connection.send(json.dumps([{"request": "message", "message": msg}]))
        #lock.release()

connection.close()
