import socket
import csv
import threading

def clientThread(clientsocket, address):
    # Message of successfull connection!
    print(f"Connection from {address} has been established.")
    
    username = clientsocket.recv(1024).decode()

    fileData = open('attendance.csv', mode='r')
    reader = csv.reader(fileData)
    
    r_row = None
    for row in reader:
        if username == row[1]:
            r_row = row
            break
    
    if r_row:
        attendance = 0
        for i in range(8):
            if r_row[i+2] == 'Done':
                attendance = attendance+1
        clientsocket.send( (str((attendance*100) / 8)).encode() )
    else:
        clientsocket.send( (str(0)).encode() )

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