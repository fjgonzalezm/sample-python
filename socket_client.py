import socket

msgFromClient       = "Hello UDP Server"
bufferSize          = 1024

bytesToSend         = [1] * bufferSize

serverAddressPort   = ("127.0.0.1", 50001)
# Create a UDP socket at client side
udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket
for i in range(100):
  udp_socket.sendto(bytearray(bytesToSend), serverAddressPort)

udp_socket.sendto(':end'.encode(), serverAddressPort)

msgFromServer = udp_socket.recvfrom(bufferSize)
msg = "Message from Server: {}".format(msgFromServer[0])
print(msg)


udp_socket.sendto(':reset'.encode(), serverAddressPort)


udp_socket.close()

# msgFromServer = UDPClientSocket.recvfrom(bufferSize)
# msg = "Message from Server {}".format(msgFromServer[0])
# print(msg)