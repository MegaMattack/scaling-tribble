import socket
import sys
import os
import Tkinter as tk
from Tkinter import *
import tkMessageBox
import threading
import Queue

class ChatWindow(tk.Frame):
    
    def __init__(self, master = None):
        tk.Frame.__init__(self,master,height=100,width=150)
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        self.createWidgets()

    def createWidgets(self):
        top=self.winfo_toplevel()
        #top.rowconfiqure(0,weight=1)
        #top.columnconfigure(0,weight=1)
        #self.rowconfigure(0,weight=1)

        #Variable Initialization
        AddressInput = StringVar()
        PortInput = StringVar()
        MessageInput = StringVar()
        ChatInput = StringVar()
        ChatInput.set(" Welcome.\nFirst message sent will be username.\n")
        s = socket.socket()

        #Widget creation
        
        self.chat=tk.Label(self,text="Hello, world!",
                           anchor=tk.W,justify=tk.LEFT,
                           textvariable=ChatInput,relief=SUNKEN)
                           
        #self.chat=tk.Text()
        self.disconnect=tk.Button(self,text="Disconnect",command=lambda:disconnect(sock))
        self.connect=tk.Button(self,text="Connect",command=
                               lambda:connect(s,AddressInput,PortInput,ChatInput))
        self.send=tk.Button(self,text="Send",command=
                            lambda:send(s,MessageInput,ChatInput))
        self.address=tk.Entry(self,textvariable=AddressInput)
        self.port=tk.Entry(self,textvariable=PortInput)
        self.message=tk.Entry(self,textvariable=MessageInput)
        self.messageLabel=tk.Label(self,text="Message")
        self.addressLabel=tk.Label(self,text="Address")
        self.portLabel=tk.Label(self,text="Port")

        #Widget binding
        self.chat.grid(columnspan=20,rowspan=40,row=1,column=0)
        self.message.grid(row=0,column=1,columnspan=5,sticky=tk.N)
        self.send.grid(row=0,column=0,sticky=tk.E+tk.N)
        self.addressLabel.grid(row=0,column=21)
        self.address.grid(row=1,column=21)
        self.portLabel.grid(row=2,column=21)
        self.port.grid(row=3,column=21)
        self.connect.grid(row=4,column=21)
        '''
        self.chat.pack(fill=Y,expand=1)
        self.messageLabel.pack(fill=X,side=TOP)
        self.addressLabel.pack(fill=X,side=LEFT)
        self.portLabel.pack(fill=X,side=LEFT)
        self.message.pack(fill=X,side=TOP)
        self.send.pack(fill=X,side=LEFT)
        self.address.pack(fill=X,side=LEFT)
        self.port.pack(fill=X,side=LEFT)
        self.connect.pack(fill=X,side=LEFT)
        '''

def connect(s,Address,Port,ChatInput):
    print "You are connected! (No, not really)"
    print "Address is " + Address.get() + ", and port is " + Port.get() + "."
    print "Socket creation complete."

    try:
        s.connect((Address.get(),int(Port.get())))
    except socket.error, msg:
        print "Bind failed. Error Code: " + str(msg[0]) + " Message: " + msg[1]
        sys.exit()

    print "Socket connection complete."
    thread = threading.Thread(target=serverthread,args=(s,Address.get(),Port.get(),ChatInput))
    thread.daemon = True
    thread.start()

def serverthread(sock,host,port,ChatInput):
    while True:
        data = sock.recv(1024)
        if not data:
            break
        ChatInput.set(ChatInput.get() + "\n" + str(data))

def send(sock,message,ChatInput):
    if message.get() == "Clear":
        ChatInput.set("")
    elif message.get() != "Quit":
        sock.send(message.get())
    else:
        sock.send(message.get())
        ChatInput.set(ChatInput.get() + "Ending session")
        #sock.close()
        quit()     
            
def Main():
    root=tk.Tk()
    client=ChatWindow(master=root)
    client.mainloop()
    root.destroy()
    
if __name__=='__main__':
    Main()

