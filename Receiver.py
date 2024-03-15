
from asyncio import sleep
import socket,cv2, pickle,struct

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = socket.gethostname() # Here Require CACHE Server IP
port = 6060
client_socket.connect((host_ip,port)) # a tuple
data = b""
payload_size = struct.calcsize("Q")
while True:
	sleep(0.04)
	while len(data) < payload_size:
		packet = client_socket.recv(4*1024) # 4K
		if not packet: break
		data+=packet
	packed_msg_size = data[:payload_size]
	data = data[payload_size:]
	msg_size = struct.unpack("Q",packed_msg_size)[0]
	
	while len(data) < msg_size:
		data += client_socket.recv(4*1024)
	frame_data = data[:msg_size]
	data  = data[msg_size:]
	frame = pickle.loads(frame_data)
	res = cv2.resize(frame, dsize=(1200,600), interpolation=cv2.INTER_CUBIC)
	cv2.namedWindow("Reciver", cv2.WINDOW_AUTOSIZE)
	cv2.imshow("Reciver",frame)
    #cv2.namedWindow("Resized_Window", cv2.WINDOW_NORMAL) 
	key = cv2.waitKey(1) & 0xFF
	if key  == ord('q'):
		break
client_socket.close()
	
