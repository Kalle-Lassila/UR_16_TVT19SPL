#test script for developing socket_controller
#This is what needs to be done in the robot program. see network_test.script or or the network_test robot program(should be in UR16s memory) for how to program the robot.
#connection1=socket_open(<ip_address>, <port>) #returns true if socket connected, can be used for infinite loop to connect in before start section
#variable = socket_read_string(timeout=0) #returns a string from TCP socket(anything what was send with this scipt)
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #initialize socket stream
s.bind(("0.0.0.0", 1440))   #open socket
s.listen(5) #listen for connection, allow 5 fails
#s.connect(("192.168.100.10",1440)) #connect to remote socket(the robot) with the robots ip and port 1440(can be pretty much anything between 1k and 64k)

client_socket, address = s.accept() #accept inbound connection

while True:
    send = input("Message: ")  #take user input
    client_socket.send(bytes(send, "UTF-8"))    #send input encoded in UTF-8

