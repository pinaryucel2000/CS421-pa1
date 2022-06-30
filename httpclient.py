import socket
import base64
import timeit


def client_program():
	
	# *** PART A ***
	host = socket.gethostname()  # as both code is running on same pc
	port = 8000  # socket server port number

	client_socket = socket.socket()  # instantiate
	client_socket.connect((host, port))  # connect to the server

	# Request to index.html
	message = "GET / HTTP/1.1\r\nHost: localhost:8000/ \r\n\r\n"
    
	client_socket.send(message.encode())  # send message
	response = client_socket.recv(8192).decode()  # receive response
	print("Response for the index.html get request:")
	print(response.split("\r\n\r\n")[0] + "\n")
	
	data = response.split("\r\n\r\n")[1] 
	
	f = open("index2.html", "w")
	f.write(data)
	f.close()
	
	body = data.split("</head>")[1].split("</html>")[0] 
	hidden = (body.strip()).split("href=\"")[1].split("\"")[0]
	print("Hidden file name: " + hidden)
	
	# *** PART B ***
	
	# Without authorization
	message = "GET /" + hidden + " HTTP/1.1\r\nHost: localhost:8000/ \r\n\r\n"
		
	client_socket.send(message.encode())  # send message
	response = client_socket.recv(8192).decode()  # receive response
	
	print("\nResponse for the get request without authorization:")
	print(response.split("\r\n\r\n")[0] + "\n")
	
	# With authorization
	credentials = "bilkentstu:cs421s2021"
	credentials_bytes = credentials.encode('ascii')
	credentials_base64_bytes = base64.b64encode(credentials_bytes)
	credentials_base64 = credentials_base64_bytes.decode('ascii')
	
	message = "GET /" + hidden + " HTTP/1.1\r\nHost: localhost:8000/\r\nAuthorization: Basic " + credentials_base64 + "\r\n\r\n"
		
	client_socket.send(message.encode())  # send message
	response = client_socket.recv(8192).decode()  # receive response
	
	print("Response for the get request with authorization:")
	print(response.split("\r\n\r\n")[0] + "\n")	
	
	data = response.split("\r\n\r\n")[1] 
	
	f = open("protected2.html", "w")
	f.write(data)
	f.close()
	
	body = data.split("</head>")[1].split("</html>")[0] 
	hidden = (body.strip()).split("href=\"")[1].split("\"")[0]
	print("Hidden file name: " + hidden)
	
	# *** PART C ***
	
	# Get information about the hidden text file
	message = "HEAD /" + hidden + " HTTP/1.1\r\nHost: localhost:8000/\r\n\r\n"
		
	client_socket.send(message.encode())  # send message
	response = client_socket.recv(8192).decode()  # receive response
	
	print("\nResponse for the " + hidden + " head request:")
	print(response.split("\r\n\r\n")[0] + "\n")
	
	content_size_text = int((response.strip()).split("Content-Length:")[1].split("\n")[0])
	
	# Get information about index.html
	message = "HEAD /" + "index.html" + " HTTP/1.1\r\nHost: localhost:8000/\r\n\r\n"
		
	client_socket.send(message.encode())  # send message
	response = client_socket.recv(8192).decode()  # receive response
	
	print("Response for the index.html head request:")
	print(response.split("\r\n\r\n")[0] + "\n")
	
	content_size_index_html = int((response.strip()).split("Content-Length:")[1].split("\n")[0])
	
	# Different ranges used to download the hidden text file
	
	for range_ in (10,100,1000,10000,15000):
		start = timeit.default_timer()
		f = open("big" + str(range_) + ".txt", "a")
		
		for i in range(0, content_size_text, range_):
			
			if i + range_ > content_size_text:
				k = content_size_text
			else: 
				k = i + range_
			
			message = "GET /" + hidden + " HTTP/1.1\r\nHost: localhost:8000/\r\nRange: bytes=" + str(i) + "-" + str(k) + "\r\n\r\n"

			client_socket.send(message.encode())  # send message
			data = (client_socket.recv(30000).decode()).split("\r\n\r\n")[1]  # receive response
			f.write(data)
			
		f.close()
		stop = timeit.default_timer()

		print("Time taken to download with range " + str(range_) + " was " + str(stop - start) + " seconds.")
		
	message = "EXIT HTTP/1.1\r\n\Host: localhost:8000\r\n\r\n"
	client_socket.send(message.encode())  # send message
	response = client_socket.recv(8192).decode()  # receive response
	print("\nResponse for the exit request:")
	print(response.split("\r\n\r\n")[0] + "\n")
	
	client_socket.close()  # close the connection

if __name__ == '__main__':
	client_program()

