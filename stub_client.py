import socket
import random

IP = "127.0.0.1"
PORT_LIST = [8000, 8001, 8002]

if __name__ == "__main__":
	
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	while True:
		msg = input("> ")
		port = PORT_LIST[random.randint(0,2)]
		addr = ("127.0.0.1", port)
		s.sendto(msg.encode(), addr)
		data, server = s.recvfrom(1024)

		print("received:", data)
