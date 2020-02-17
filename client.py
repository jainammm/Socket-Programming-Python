import socket

def main():
    hostname = input("Please Enter Host IP: ")
    port = int(input("Enter Port Number: "))

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print(clientSocket.connect((hostname, port)))
    except ConnectionRefusedError:
        print("Please specify correct hostname and port number!")
        return

    # Message of successfull connection!
    print(f"Connection with {hostname} has been established.")

    # Enters username and sends to the server
    print("=========================================")
    username = input("Please enter the username: ")
    clientSocket.send(username.encode())

    # Print ack received by the server
    ack = clientSocket.recv(1024).decode()
    print("=========================================")
    print(f"{ack}")

    # Enter the password and send to the server
    print("=========================================")
    password = input("Please enter the password: ")
    clientSocket.send(password.encode())

    ack = clientSocket.recv(1024).decode()
    print("=========================================")
    print(f"{ack}")
    
    # Close connection with server
    clientSocket.close()

if __name__== "__main__":
    main()