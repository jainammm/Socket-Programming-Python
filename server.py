import socket
import csv

usernamePasswordDict = {}

with open('login_credentials.csv', 'r') as file_data:
    reader = csv.DictReader(file_data, ("Username", "Password"))
    for i in reader:
        usernamePasswordDict[i["Username"]] = i["Password"]

def checkPassword(username, password):
    try:
        uPass = usernamePasswordDict[username]
    except:
        uPass = "NA"

    if uPass == password: 
        return "ACK: User has logged in!"
    
    return "ACK: Please enter correct password or username!"

def main():
    hostname = socket.gethostname()
    port = int(input("Enter Port number: "))

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((hostname, port))
    serverSocket.listen(5)

    print(f"The server has started running with host {hostname} and port {port}")
    print("=========================================")

    while True:
        clientsocket, address = serverSocket.accept()

        # Message of successfull connection!
        print(f"Connection from {address} has been established.")
        
        username = clientsocket.recv(1024).decode()
        
        # Send acknowledgement of received username.
        ack = "ACK: Username Received"
        clientsocket.send(ack.encode())

        password = clientsocket.recv(1024).decode()

        # Check password and send acknowledgement
        ack = checkPassword(username, password)
        clientsocket.send(ack.encode())
        
        # Close socket and listen to other sockets
        clientsocket.close()
        



if __name__ == "__main__":
    main()