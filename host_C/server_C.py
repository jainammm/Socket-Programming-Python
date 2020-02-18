import socket
import csv
import threading

usernamePasswordDict = {}

with open('login_credentials_C.csv', 'r') as file_data:
    reader = csv.DictReader(file_data, ("Username", "Password"))
    for i in reader:
        usernamePasswordDict[i["Username"]] = i["Password"]

def getPassword(username):
    try:
        password = usernamePasswordDict[username]
    except:
        password = "NA"

    return password

def clientThread(clientsocket, address):
    # Message of successfull connection!
    print(f"Connection from {address} has been established.")
    
    username = clientsocket.recv(1024).decode()
    print(f"Received username from {address}.")

    # Send acknowledgement of received username.
    password = getPassword(username)
    clientsocket.send(password.encode())
    print(f"Password sent to {address}.")

    clientsocket.close()
    print(f"Connection from {address} has been closed.")

def main():
    hostname = "0.0.0.0"
    port = int(input("Enter Port number: "))

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((hostname, port))
    serverSocket.listen(5)

    ipAddr = socket.gethostbyname(hostname)
    print(f"The server has started running with host {ipAddr} and port {port}")
    print("=========================================")

    try:
        while True:
            clientsocket, address = serverSocket.accept()

            newThread = threading.Thread(target=clientThread, args=(clientsocket, address, )) 
            newThread.start()
    except KeyboardInterrupt:
        serverSocket.close()



if __name__ == "__main__":
    main()