import socket
import json
import time
from sys import exit
from tinydb import TinyDB,Query
import datetime
import pprint

db_user = TinyDB('D:/IT/python/SocketApp/user_database.json')
table_user = db_user.table('users')
User = Query()

db_message = TinyDB('D:/IT/python/SocketApp/message_database.json')
message_user = db_message.table('messages')

# Launch program date
created = datetime.datetime.now() 
start = time.perf_counter() 


# get the hostname
host = socket.gethostname()
port = 5000  # initiate port no above 1024
server_socket = socket.socket()  # get instance
server_socket.bind((host, port))  # bind host address and port together
server_socket.listen(2)
conn, address = server_socket.accept()  

def msg_read(login):
    pprint.pprint(message_user.search(User.login==login))
    user_dashboard(login)

def msg_send(login):
    while True:
        msg = input("Type message ->")[:255]
       
        dictionary = {
        "login:" : login,   
        "message:" : msg
        }
        result = json.dumps(dictionary) # converting object into a json string
        conn.send(result.encode())
        
        message_user.insert({'login': login, 'message': msg})
        user_dashboard(login)
  

def user_dashboard(login):
    if message_user.count(User.login == login) > 5:
                print(f"{login} - inbox overflow \n")
                user_mode()
    print("Send message (msg-send) | Read message (msg-read)")
    option = input("->")
    
    if option.lower() == "msg-send":
        msg_send(login)
    elif option.lower() == "msg-read":
        msg_read(login)
    else:
        exit(0) # stop server app


def uptime_fun(): 
    end = time.perf_counter()
    duration = end-start
    duration = round(duration,2)
    dictionary = {
        "life time:" : str(duration) +"s"
    }
    pprint.pprint(dictionary)
    server_program()


def info_fun():  
    dictionary = {
        "created:" : str(created)
    }
    pprint.pprint(dictionary)
    server_program()


def help_fun(): 
    dictionary = {
        "options: " :     
        {
            "option 1": "uptime - zwraca czas zycia serwera",
            "option 2": "info - zwraca date utworzenia serwera",
            "option 3": "stop - zatrzymuje serwer i klienta",
        }
    }
    pprint.pprint(dictionary)
    server_program()



def user_mode():
    print("Create | Login")
    option = input("->")
    print("\n")

    if option.lower()=="create":
        print("New user - login")
        new_login = input("->")
        print("\n")

        print("New user - password")
        new_password = input("->")
        print("\n")
        
        table_user.insert({'login': new_login, 'password': new_password})
        user_mode()

    elif option.lower()=="login":
        print("Login:")
        login = input("->")
        print("\n")
       
        print("Password:")
        password = input("->")
        print("\n")

        if table_user.contains(User.login == login) and table_user.contains(User.password == password):
            user_dashboard(login)  
        else:
            print("Error")
            time.sleep(2)
            user_mode()



def admin_mode():
    pprint.pprint(message_user.all())
    server_program()

# switch-case declaration
switcher = {
    "uptime": uptime_fun,
    "info": info_fun,
    "help": help_fun,
    "user": user_mode,
    "admin": admin_mode
    }



def server_program():
    print("Connection from: " + str(address) + "\n")
    
    print("User | Admin | Help")
    mode = input("->")
    print("\n")

    redirection = switcher.get(mode.lower(),"Invalid command")
    redirection()
    
    conn.close()  # close the connection

   
if __name__ == '__main__':
    server_program() 