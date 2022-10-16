import sys
import socket

# How many bytes is the word length?
WORD_LEN_SIZE = 2

def usage():
    print("usage: wordclient.py server port", file=sys.stderr)

packet_buffer = b''

# helper function
def get_length_from_first_two_bytes(packet, verbose=False):
  """
  Returns the integer value of the first two bytes of a bytestring. 
  """
  # getting first two bytes, which represent length of the following word, as a bytestring
  length_byteform = packet[0:2]
  if verbose:
    print("length_byteform:", length_byteform)

  # converting the first two bytes to the length of the following word in integer form 
  length_integer = int.from_bytes(length_byteform, 'big')
  if verbose:
    print("length_integer:", length_integer)
  return length_integer

# helper function 
def get_word_from_length(packet, length, verbose=False):
  """
  Gets word in byteform from packet, offset by two to account for first two bytes representing 
  the word length
  """
  word_byteform = packet[2:2+length]
  if verbose:
    print("word_byteform:", word_byteform)
  
  return word_byteform

def has_enough_data_to_make_packet():
  global packet_buffer
  length_of_collected_data = len(packet_buffer)
  desired_length = get_length_from_first_two_bytes(packet_buffer)
  return desired_length + 2 <= length_of_collected_data

def pop_word_packet(length):
  global packet_buffer
  curr_packet = packet_buffer[0:length]
  packet_buffer = packet_buffer[length:]
  return curr_packet

def get_next_word_packet(s):
    """
    Return the next word packet from the stream.

    The word packet consists of the encoded word length followed by the
    UTF-8-encoded word.

    Returns None if there are no more words, i.e. the server has hung
    up.
    """

    global packet_buffer

    # looping until buffer finds something to return (either a word, or `None`)
    while True:
      # receive packet
      d = s.recv(5)

      # append data to buffer
      packet_buffer += d

      # break if buffer (which just had the received data appended to it) is empty
      if (len(packet_buffer) == 0):
        return None

      # check that buffer has enough bytes (2 bytes) to calculate word length 
      if (len(packet_buffer) >= 2):
        # check of buffer has enough data to make a packet for its length
        if has_enough_data_to_make_packet():
          # get length of the word (that follows the first two bytes)
          curr_length = get_length_from_first_two_bytes(packet_buffer)
          # pop the word packet off of the global buffer
          curr_packet = pop_word_packet(curr_length + 2)
          return curr_packet 
      
      # check that there isn't leftover packet data to get caught in infinite loop
      if (len(packet_buffer) != 0 and len(d) == 0):
        return None

def extract_word(word_packet):
    """
    Extract a word from a word packet.

    word_packet: a word packet consisting of the encoded word length
    followed by the UTF-8 word.

    Returns the word decoded as a string.
    """

    length_of_word = get_length_from_first_two_bytes(word_packet)
    word = get_word_from_length(word_packet, length_of_word)
    return word.decode()

# Do not modify:

def main(argv):
    try:
        host = argv[1]
        port = int(argv[2])
    except:
        usage()
        return 1

    s = socket.socket()
    s.connect((host, port))

    print("Getting words:")

    while True:
        word_packet = get_next_word_packet(s)

        if word_packet is None:
            break

        word = extract_word(word_packet)

        print(f"    {word}")

    s.close()

if __name__ == "__main__":
    sys.exit(main(sys.argv))
