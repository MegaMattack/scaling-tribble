import socket
import Queue
import threading
import inspect

#TODO: Protect against race conditions

def Main():
    host = ''
    port = 8888
    messages=Queue.Queue()
    registered=Queue.Queue()
    processed=Queue.PriorityQueue()
    lock = threading.Lock()

    sock = socket.socket()
    sock.bind((host,port))

    t = threading.Thread(target = Broadcast,args = (messages,registered,processed,lock))
    t.daemon=True
    t.start()
    ConnectionMonitor(lock,sock,messages,registered,processed)

def ServerIO(lock,conn,addr,messages,registered,processed,username):
    while True:
        data = conn.recv(1024)
        if data == "Quit":
            break
        with lock:
            FormatData = username + ": " + str(data)
            print FormatData
            messages.put(FormatData,True,30)
    messages.put(username + " has disconnected. ")
    #TODO: The quit dialog is broken. Must be completely reworked.
    print "Thread for " + str(addr) + " has ended."
    conn.close()
    #print "Thread for " + str(addr) + " has ended."

def ConnectionMonitor(lock,sock,messages,registered,processed):
    while True:
        sock.listen(5)
        conn,addr = sock.accept()
        print "Connection from: " + str(addr)
        data = conn.recv(1024)
        if not data:
            break
        #registered.put((registered.qsize(),conn),True)
        registered.put(conn,True)
        messages.put(str(data)+" has joined the server.",True,30)
        #print "Username is " + str(data)
        username = str(data)
        t = threading.Thread(target = ServerIO, args = (lock,conn,addr,messages,registered,processed,username))
        t.daemon=True
        t.start()
        print "Thread started"

def Broadcast(messages,registered,processed,lock):
    while True:
        #if(messages.empty()==False):
        m = messages.get(True)
        with lock:
            print "BROADCAST: " + m
            while(registered.empty()==False):
                print "Running loop1"
                try:
                    recipient = registered.get(False)
                    recipient.send(m)
                    processed.put(recipient)
                except:
                    "Error sending message"
            while(processed.empty()==False):
                print "Running loop2"
                #registered.put((registered.qsize(),processed.get(False)),False)
                registered.put(processed.get(False),False)
            
if __name__ == '__main__':
    Main()
#threading.active_count()
