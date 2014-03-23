#server.py
import socket
import json
import threading
import time


#Send a message to all clients
def send_all(msg):
    for t in threads:
	if t.isAlive():
        	t.send(msg)

#This handles all the clients, receive and responds to requests
class HandleThread(threading.Thread):

    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connection = conn
        self.loggedin = False
        self.username = ''

    def run(self):
	global users
	running = True
        while running:
	    jmsg = json.loads(self.connection.recv(1024))
            print jmsg
            if jmsg[0].get('request', '') == "login":
                self.username = jmsg[0].get('username', '')
		if (not self.valid_username(self.username)):
		    self.send(json.dumps([{"response": "message", "username": self.username,"error": "Invalid username!"}]))
		elif not self.available_username(self.username):
		    self.send(json.dumps([{"response": "message", "username": self.username,"error": "Name already taken!"}]))
		else:
	            self.loggedin = True
		    users.append(self.username)
	            self.send(json.dumps([{"response": "login", "username": self.username}]))
	            if(len(messages) > 0):
	                for i in messages:
	                    self.send(json.dumps([{"response": "message", "username": '',"message":i}]))
	                    time.sleep(0.001)
            elif jmsg[0].get('request', '') == "message":
                if(self.loggedin):
                    messages.append(self.username + ": " + jmsg[0].get('message', ''))
                    send_all(json.dumps([{"repsonse": "message", "message": jmsg[0].get('message'), "username": self.username}]))
                else:
                    self.send(json.dumps([{"response": "message", "error": "You are not logged in"}]))

            if jmsg[0].get('request', '') == "logout":
                # do logout stuff and respond
		if(self.loggedin):
		    self.send(json.dumps([{"response": "logout", "username": self.username}]))
		    self.connection.close()
		    users.remove(self.username)
		    running = False
		else:
		    self.send(json.dumps([{"response": "logout", "error": "Not logged in!", "username": self.username}]))
                    
    #Sends a message to a client
    def send(self, msg):
        self.connection.send(msg)

    #Checks if a username is valied
    def valid_username(self, name):
    	import re
   	return re.match('^\w+$', name)

    #Checks if a username is allready in use
    def available_username(self, name):
    	return name not in users


#start of program (server)

#Sets opp some variables
threads = [] #list of threads (sockets to clients)
messages = [] #logg
users = [] #list of used usernames

#Set up socket
HOST = 'localhost'
PORT = 9996
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))

#Run as long as the server is running
#Listen for new conection and gives each new conection a new thread
while True:
    s.listen(1)
    conn, addr = s.accept()
    t = HandleThread(conn)
    t.start()
    threads.append(t)
    print 'Connected by', addr


