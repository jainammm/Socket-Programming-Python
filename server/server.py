import socket
import csv
import threading

def getConfig(filename):
    fileData = open(filename)
    configLine = fileData.readline()

    configLine = configLine.replace(" ", "")

    config = configLine.split("|")

    return config

def clientThread(clientsocket, address):
    # Message of successfull connection!
    print(f"Connection from {address} has been established.")
    
    username = clientsocket.recv(1024).decode()
    if username == "EXIT":
        clientsocket.close()
        print(f"Connection from {address} has been closed.")
        print("=========================================") 
        return
    
    # Send acknowledgement of received username.
    ack = "ACK: Username Received"
    clientsocket.send(ack.encode())

    password = clientsocket.recv(1024).decode()
    if password == "EXIT":
        clientsocket.close()
        print(f"Connection from {address} has been closed.")
        print("=========================================") 
        return

    hostSocket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if username <= "2017csb1081@iitrpr.ac.in":
        config = getConfig("routing_table/A.rtl")
    elif username <= "2017csb1103@iitrpr.ac.in":
        config = getConfig("routing_table/B.rtl")
    else:
        config = getConfig("routing_table/C.rtl")

    print(f"Checking of  password from Host {config}!")

    hostSocket1.connect((config[1], int(config[2])))
    print(f"Connected to {config}.")

    hostSocket1.send(username.encode())
    print(f"Sending username - {username} to host {config}.")

    uPass = hostSocket1.recv(1024).decode()
    print(f"Received ack from {config}.")

    hostSocket1.close()

    # Checking attendance
    hostSocket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    configD = getConfig("routing_table/D.rtl")
    hostSocket2.connect((configD[1], int(configD[2])) )

    print(f"Connected to {configD}.")
    
    hostSocket2.send(username.encode())
    print(f"Sending username - {username} to host {configD}.")

    attendancePercentage = float(hostSocket2.recv(1024).decode())
    print(f"Received ack from {configD}.")

    hostSocket2.close()

    if uPass == password and attendancePercentage >= 80:
        ack = "ACK: Login Successful!"
    elif uPass == password and attendancePercentage <= 80:
        ack = "ACK: Attendance Short!"
    else:
        ack = "ACK: Please enter correct password or username!"

    # Send acknowledgement
    clientsocket.send(ack.encode())

    # Close socket and listen to other sockets
    clientsocket.close()
    print(f"Connection from {address} has been closed.")
    print("=========================================")  

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