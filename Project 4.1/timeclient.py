import socket

server_name, port = 'time.nist.gov', 37
s = socket.socket()
s.connect((server_name, port))

byte_data_send = ("""
GET / HTTP/1.1
Host: {}
Connection: close

""").format(server_name)

text_data_send = byte_data_send.encode()

s.sendall(text_data_send)

def recv_all_bytes(rec_s):
  # taken from in class 
  data = b''
  while True: 
    chunk = rec_s.recv(4096)
    if chunk == b'':
      break
    data += chunk
  return data

byte_data_rec = recv_all_bytes(s)

print("Time: ", int.from_bytes(byte_data_rec, 'big'))