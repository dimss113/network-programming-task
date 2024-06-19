import socket

def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 45000))
    
    while True:
        # get input from user
        user_input = input("Enter your request (TIME or QUIT): ").strip()
        
        if user_input == "TIME":
            request = "TIME\r\n"
        elif user_input == "QUIT":
            request = "QUIT\r\n"
        else:
            print("Invalid input. Please enter 'TIME' or 'QUIT'.")
            continue
        
        # send resonse to server
        client.sendall(request.encode('utf-8'))
        
        # recieve response from server
        response = client.recv(1024).decode('utf-8')
        print("Response from server:", response)
        
        if "Server terminating connection" in response:
            break
    
    # close connection
    client.close()

if __name__ == "__main__":
    run_client()
