# Echo server program
import socket
import json
import threading
import time

HOST = 'localhost'                 # Symbolic name meaning all available interfaces
PORT = 9997              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))

def valid_username(name):
    import re
    return re.match('^\w+$', name)

def available_username(name):
    return name not in users

threads = []
messages = []
users = []

def send_all(msg):
    for t in threads:
        t.send(msg)

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
                #check username
                self.username = jmsg[0].get('username', '')
		if (not valid_username(self.username)):
		    print "invalid"
		    self.send(json.dumps([{"response": "message", "username": self.username,"error": "Invalid username!"}]))
		elif not available_username(self.username):
		    print "unav"
		    self.send(json.dumps([{"response": "message", "username": self.username,"error": "Name already taken!"}]))
		else:
		    print "ok"
	            self.loggedin = True
		    users.append(self.username)
	            self.send(json.dumps([{"response": "login", "username": self.username}]))
	            print len(messages)
	            if(len(messages) > 0):
	                for i in messages:
	                    print i
	                    self.send(json.dumps([{"response": "message", "username": '',"message":i}]))
	                    time.sleep(0.001)
            elif jmsg[0].get('request', '') == "message":
                if(self.loggedin):
                    messages.append(self.username + ": " + jmsg[0].get('message', ''))
                    #print(messages)
                    send_all(json.dumps([{"repsonse": "message", "message": jmsg[0].get('message'), "username": self.username}]))
                else:
                    self.send(json.dumps([{"response": "message", "error": "You are not logged in"}]))

            if jmsg[0].get('request', '') == "logout":
                # do logout stuff and respond
		if(self.loggedin):
		    self.send(json.dumps([{"response": "logout", "username": self.username}]))
		    print "sendt"
		    self.connection.close()
		    users.remove(self.username)
		    running = False
		else:
		    self.send(json.dumps([{"response": "logout", "error": "Not logged in!", "username": self.username}]))
                    

    def send(self, msg):
        self.connection.send(msg)


while True:
    s.listen(1)
    conn, addr = s.accept()
    #connections.append(conn)
    #handle(conn) #make as thread
    t = HandleThread(conn)
    t.start()
    threads.append(t)
    print 'Connected by', addr


