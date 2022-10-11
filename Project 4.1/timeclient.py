import socket, datetime

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

# taken from assignment
def system_seconds_since_1900():
    """
    The time server returns the number of seconds since 1900, but Unix
    systems return the number of seconds since 1970. This function
    computes the number of seconds since 1900 on the system.
    """

    # Number of seconds between 1900-01-01 and 1970-01-01
    seconds_delta = 2208988800

    seconds_since_unix_epoch = int(datetime.datetime.now().strftime("%s"))
    seconds_since_1900_epoch = seconds_since_unix_epoch + seconds_delta

    return seconds_since_1900_epoch

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
server_seconds_elapsed = int.from_bytes(byte_data_rec, 'big')
system_seconds_elapsed = system_seconds_since_1900()
s.close()

print("NIST time  :", server_seconds_elapsed)
print("System time:", system_seconds_elapsed)