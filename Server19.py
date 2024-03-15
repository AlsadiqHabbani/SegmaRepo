# Receiver Code
from asyncio import sleep
import cv2
import socket
import pickle
import struct
def receive_video():
    global frame

    # Create a socket connection
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((socket.gethostname(),8000))  # Use your desired IP and port "Habbani"
    server_socket.listen(5)

    print("Server listening...")

    # Accept a connection from a client
    connection, addr = server_socket.accept()
    print(f"Connection from {addr}")

    data = b""
    payload_size = struct.calcsize("Q")

    while True:
        sleep(0.04)
        while len(data) < payload_size:
            packet = connection.recv(4 * 1024)  # 4K buffer size
            if not packet:
                break
            data += packet

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        while len(data) < msg_size:
            data += connection.recv(4 * 1024)

        frame_data = data[:msg_size]
        data = data[msg_size:]

        # Deserialize the frame
        frame = pickle.loads(frame_data)

        # Display the received frame (optional)
        cv2.imshow('Server', frame)
        key = cv2.waitKey(1) & 0xFF
        if key  == ord('q'):
            break
def send_video(conn, addr):
    global frame
    # Create a socket connection
    #server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #server_socket.bind(('0.0.0.0', 9990))  # Use your desired IP and port
    #server_socket.listen(5)

    print("2nd Server listening...")

    # Accept a connection from a client
    #connection, addr = server_socket.accept()
    print(f"Connection from {addr}")
    x=1
    while True:
        try:
	
            data = pickle.dumps(frame)

        # Pack the frame size (as a 4-byte integer) and frame data
            message = struct.pack("Q", len(data)) + data

        # Send the frame to the server
            conn.sendall(message)
        except Exception as e:
            print(e)
            conn.close()
            pass
             
            
            
    

if __name__ == "__main__":
    # Start sender and receiver in separate threads or processes
    import threading
    global frame

    receiver_thread = threading.Thread(target=receive_video)

    receiver_thread.start()
    PORT = 9990
    SERVER = socket.gethostname()
    ADDR = (SERVER, PORT)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    while True:
        print('Prepare for second server')
        conn, addr = server.accept()
        send_thread = threading.Thread(target=send_video,args=(conn, addr))
        send_thread.start()
    
    