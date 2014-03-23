# Echo server program
import socket
import json
import threading

HOST = 'localhost'                 # Symbolic name meaning all available interfaces
PORT = 9999              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))

threads = []

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
	running = True
        while running:
	    m = self.connection.recv(1024)
	    jmsg = json.loads(m)
            print jmsg
            if jmsg[0].get('request', '') == "login":
                #check username
                self.username = jmsg[0].get('username', 'Anonymous')
                self.loggedin = True
                self.send(json.dumps([{"response": "login", "username": self.username}]))

            if jmsg[0].get('request', '') == "message":
                if(self.loggedin):
                    send_all(json.dumps([{"repsonse": "message", "message": jmsg[0].get('message'), "username": self.username}]))
                else:
                    self.send(json.dumps([{"response": "message", "error": "You are not logged in"}]))

            if jmsg[0].get('request', '') == "logout":
                # do logout stuff and respond
		if(self.loggedin):
		    self.send(json.dumps([{"response": "logout", "username": self.username}]))
		    print "sendt"
		    self.connection.close()
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

