#client.py
import socket
import threading
import json


#This function is used in a thread an listens for new messages
#It prints out the new messages
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


#Start of program
print 'Hello and welcome to this chatting applciation!'

#Fix connection
host = 'localhost'
port = 9996
connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect((host, port))

#Fix threads
loggedin = False
exit = False
ko = []
lock = threading.Lock()
thread = threading.Thread(target = recieve)
thread.setDaemon(True)

#Do login sequence
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
	

print "You are logged in!"

#Starts the thread for lisning for new messages
thread.start()

#Ask the user for a message and sends the message to the server
while(exit == False):
    msg = raw_input('')
    if(msg == "\logout"):
	print msg
        connection.send(json.dumps([{'request': 'logout'}]))
    else:
        connection.send(json.dumps([{"request": "message", "message": msg}]))


#Close the socket, on client side
connection.close()
