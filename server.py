import socket
import json
import time
from sys import exit
from tinydb import TinyDB,Query
import datetime

db = TinyDB('D:/IT/python/SocketApp/userdatabase.json')
table = db.table('users')

# Launch program date
created = datetime.datetime.now() 
start = time.perf_counter() 

def msg_read():
    pass

def msg_send():
    pass


def uptime_fun(): 
    end = time.perf_counter()
    duration = end-start
    duration = round(duration,2)
    dictionary = {
        "life time:" : str(duration) +"s"
    }
    result = json.dumps(dictionary) # converting object into a json string
    return result

def info_fun():  
    dictionary = {
        "created:" : str(created)
    }
    result = json.dumps(dictionary)
    return result

def help_fun(): 
    dictionary = {
        "options: " :     
        {
            "option 1": "uptime - zwraca czas zycia serwera",
            "option 2": "info - zwraca date utworzenia serwera",
            "option 3": "stop - zatrzymuje serwer i klienta",
            "option 4": "msg-read - read all messages",
            "option 5": "msg-send - send a message" 
        }
    }
    result = json.dumps(dictionary)
    return result

# switch-case declaration
switcher = {
    "uptime":  uptime_fun,
    "info":  info_fun,
    "help":  help_fun,
    "msg-read":  msg_read,
    "msg-send":  msg_send,
    }


   


def user_mode():
    print("Create | Login")
    option = input("->")
    if option.lower()=="create":
        print("New user - login")
        new_login = input("->")
        print("New user - password")
        new_password = input("->")
        # append to user database above login and pass

    elif option.lower()=="login":
        print("Login:")
        login = input("->")
        print("Password:")
        password = input("->")
        # if  login in database['login'] and password in database['password']:
        while(True):
            # receive data stream. it won't accept data packet greater than 1024 bytes
            data = conn.recv(1024).decode()
            message = input(" -> ")  # take input
        
            if not message:
                break

            if data == "stop":
                exit(0) # stop server app
            else:
                answer = switcher.get(data,"Invalid command")
                result = answer()
                conn.send(result.encode())
            conn.close()  # close the connection

def admin_mode():
    print("All messages | other option")
    option = input("->")

def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    
    print("User | Admin ?")
    mode = input("->")
    
    if mode.lower()=="user":
        user_mode()
    elif mode.lower()=="admin":
        admin_mode()

if __name__ == '__main__':
    server_program() 