import socket
import sys
import time

# convert to IPs later
# make sure to include localhost!
server_list = [8000, 8001, 8002]

LOCAL_SEQ = 0
GLOBAL_SEQ = 0
N_SERVERS = 3

# PLACEHOLDER
S_ID = -1

# buffer to hold outgoing request messages in case of NAK
# entries are removed after TIMEOUT seconds (TIMEOUT should be ~RTT)
send_queue = {}
TIMEOUT = 20

# buffer to hold out of order messages
# indexed by global sequence number
req_queue = {}

def formRequest(query):

	if(query[0:5] == "DEBUG"):
		m_tokens = query.split()
		req = "DEBUG\n"
		req += m_tokens[1] + "\n"
		req += m_tokens[2] + "\n"
		req += m_tokens[3] + "\n"
		return req

	req = "REQUEST\n"
	req += str(S_ID) + "\n"
	req += str(LOCAL_SEQ) + "\n"
	req += query
	return req

def formSequence(req_id, send_id):
	global GLOBAL_SEQ
	req = "SEQUENCE\n"
	req += str(GLOBAL_SEQ+1) + "\n"
	# request ID
	req += req_id + "\n"
	req += send_id + "\n"
	return req

def queryDatabase(query):
	print(query)
	pass

def refreshQueue():
	global send_queue
	t = time.time()
	tmp_dict = {}
	for i in send_queue:
		packet, timestamp = send_queue[i]
		if(t-timestamp < TIMEOUT):
			tmp_dict[i] = send_queue[i]
	send_queue = tmp_dict

if __name__ == "__main__":

	# global GLOBAL_SEQ
	# global N_SERVERS

	# eventually have predefined port on different IPs
	S_ID = int(sys.argv[1])
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind(('', S_ID+8000))
	print("starting server on port", str(S_ID+8000))
	client_address = None

	while True:

		message, addr = s.recvfrom(1024)
		print("message from", addr)

		message = message.decode()
		q_tokens = message.split("\n")

		# save client request here?
		# otherwise we need to pass request information 
		#     (db queries) as SEQUENCE param to execute
		# put requests into list
		# pop from list when sequence for request list is received
		if(q_tokens[0] == "REQUEST"):
			print("received request:\n%s" % message)

			# How to get request message id??
			# currently take local seq num as placeholder
			m_tokens = message.split("\n")
			send_id = m_tokens[1]
			req_id = m_tokens[2]

			# missing packet, transmit ACK
			if(int(req_id) > LOCAL_SEQ):
				nak = "NAK\n" + str(LOCAL_SEQ)
				s.sendto(nak.encode(), addr)
			else:

				# send sequence message
				LOCAL_SEQ += 1
				if(GLOBAL_SEQ % N_SERVERS == S_ID):

					print("server selected for sequence numbering")

					# wait for ACK from all servers
					num_acks = 1
					while(num_acks < N_SERVERS):
						m, a = s.recvfrom(1024)
						m = m.decode()
						if(m == "ACK"):
							num_acks += 1

					req = formSequence(send_id, req_id)
					for port in server_list:
						print("sending to server on port", port)
						s.sendto(req.encode(), ("127.0.0.1", port))
				
				# send ACK to designated server
				else:
					# sleep to allow leader to start blocking
					time.sleep(0.5)

					leader_id = GLOBAL_SEQ % N_SERVERS 

					s.sendto("ACK".encode(), ("127.0.0.1", server_list[leader_id]))

		elif(q_tokens[0] == "SEQUENCE" or q_tokens[0] == "DEBUG"):

			print("received sequence:\n%s" % message)

			m_tokens = message.split("\n")
			new_global = int(m_tokens[1])
			req_id = int(m_tokens[2])
			send_id = int(m_tokens[3])

			# if new global sequence number is next
			if(new_global == GLOBAL_SEQ + 1):
				GLOBAL_SEQ = new_global
				# perform database function
				print("DELIVERING REQUEST", GLOBAL_SEQ)

				# deliver outstanding messages in queue if they exist
				i = GLOBAL_SEQ + 1
				while(req_queue):
					if(i not in req_queue):
						break
					q_request = req_queue.pop(i, None)
					#perform database function
					print("DELIVERING REQUEST %d FROM QUEUE" % i)
					GLOBAL_SEQ +=  1
					i += 1

			# if old message, do nothing
			elif(new_global <= GLOBAL_SEQ):
				pass
			# delay requests
			else:
				print("Out of order message detected... adding to queue")
				# store message in queue indexed by order
				req_queue[new_global] = message

			# deliver response to client
			if(client_address is not None):
				s.sendto("response!".encode(), client_address)
				client_address = None

		# retransmit packet
		elif(q_tokens[0] == "NAK"):
			index = int(q_tokens[1])
			packet, timestamp = send_queue[index]
			s.sendto(packet.encode(), addr)

		else:
			# form request message and send to all servers
			client_address = addr

			req = formRequest(message)
			for port in server_list:
				print("sending to server on port", port)
				s.sendto(req.encode(), ("127.0.0.1", port))
				send_queue[LOCAL_SEQ] = (req, time.time())

		refreshQueue()