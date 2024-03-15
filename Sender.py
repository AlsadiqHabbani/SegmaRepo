# Sender Code
from asyncio import sleep
import cv2
import socket
import pickle
import struct

# Sender Code
def send_video():
    # Initialize the camera
    try:
        cap = cv2.VideoCapture(0)
        print('camera is opened')
        # Create a socket connection
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((socket.gethostname(),8000)) # Replace with your server's IP and port

        while True:
            sleep(0.04)
            # Read a frame from the camera
            try:
                ret, frame = cap.read()
                # Serialize the frame
                data = pickle.dumps(frame)

                # Pack the frame size (as a 4-byte integer) and frame data
                message = struct.pack("Q", len(data)) + data

                # Send the frame to the server
                client_socket.sendall(message)

                # Display the frame locally (optional)
                cv2.imshow('Sender', frame)
                cv2.waitKey(1)
                key = cv2.waitKey(1) & 0xFF
                if key  == ord('q'):
                    break
            except  Exception as e:
                print(e)
                client_socket.close()
                break
        

        cap.release()
    except  Exception as e:
            print(e)
            client_socket.close()
            pass    
if __name__ == "__main__":

    # Start sender and receiver in separate threads or processes
    import threading

    sender_thread = threading.Thread(target=send_video)
 
    sender_thread.start()