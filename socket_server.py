import socket, sys, hashlib, os

# Create a datagram socket
def open_socket(family=socket.AF_INET, socket_type=socket.SOCK_DGRAM, reopening=False):
  '''Open a new UDP socket'''
  global udp_socket
  
  if udp_socket is not None:
    udp_socket.close()
    
  udp_socket = socket.socket(family=family, type=socket_type)
  udp_socket.bind((localIP, localPort))

  # Bind to address and ip
  if reopening:
    print("Recovered socket connection on udp://{}:{}".format(localIP, localPort))
  else:
    print("UDP server up and listening on udp://{}:{}".format(localIP, localPort))
    
def read(bufferSize):
  '''Reads from the open socket'''
  global udp_socket
  return udp_socket.recvfrom(bufferSize)

class SocketMessage:
  def __init__(self, message):
    if message is None:
      self.message = ''
    else:
      self.message = message.decode()
  
  def len(self):
    return len(self.message)
    
  def iscommand(self):
    return self.message.startswith(':')
  
  def isreset(self):
    return self.message.startswith(':reset')
    
  def isend(self):
    return  self.message.startswith(':end')

if __name__ == '__main__':
  localIP     = socket.gethostname()
  localPort   = int(os.getenv('PORT', 50001))
  bufferSize  = 1024
  udp_socket     = None
  bytes_received = {}

  open_socket()

  # Listen for incoming datagrams
  while(True):
    try:    
      bytesAddressPair = read(bufferSize)

      message = bytesAddressPair[0]
      
      if message is None or len(message) < 1:
        continue
        
      message = SocketMessage(message)
      
      address, port = bytesAddressPair[1]
      
      client_key = hashlib.sha1('{}-{}'.format(address,port).encode()).hexdigest()

      if client_key not in bytes_received:
        bytes_received[client_key]=0

      if message.iscommand() and message.isend():
        print('detected end communication')
        clientMsg = "Received {} bytes from client {}".format(bytes_received[client_key], client_key)
        udp_socket.sendto(clientMsg.encode(), (address,port))
        print(clientMsg)

      elif message.iscommand() and message.isreset():
        print('client requested reset')
        del bytes_received[client_key]

      else:
        bytes_received[client_key] += message.len()
        
    except Exception as error:
      print('ERROR: ', error)
      print('Trying to reset socket connection')
      open_socket(reopening=True)
