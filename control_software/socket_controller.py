#socket_controller module for handling comms with ur16e and ur10 robots
#Oulu University of Applied Sciences
#TVT19SPL
import socket, threading

class RobotConnectionManager():
    '''Creates socket for communicating with the robot and handles recieved TCP messages'''
    def __init__(self, port: int, buffer: int):
        self.robot_port = port  #port used to communicate with the ur control box
        #TODO logic for determining message size dynamically, must also probably be implemented on the robot side
        #messages are recieved one at a time anyways so just using a big enough buffer to chatch all is prob enough
        self.buffer_size = buffer   #size of the message buffer used(the number of bytes in each message sent by the robot)
        
    def connection(self):
        '''Starts and in the future manages socket connection to the robot or any socket for that matter'''
        #TODO unexpected disconnections are not handled at all
        self.base_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #initialize socket object
        self.base_socket.bind(("0.0.0.0", self.robot_port))    #bind the socket to unroutable address for now, and listen to robot_port
        self.base_socket.listen(5) #start listening and allow 5 failed attempts to connect
        self.robot_socket, self.robot_address = self.base_socket.accept()
        while True:
            #TODO recive data and send data prob need their own threads or async methods
            message = self.robot_socket.recv(self.buffer_size)  #get buffer_size of bytes from socket buffer
            message = message.decode("utf-8")   #decode bytes to utf-8 character string
            print(message)
    
    def send(self):
        '''Take user input and sen it to socket'''
        #TODO command messages should only be sent when the robot is ready to recieve new instructions
        while True:
            message = input()
            self.robot_socket.send(bytes(message,"utf-8"))  #use the socket created in rcm to send string as bytes
    
    def start(self):
        '''Automatically creates needed threads so user does not need to worry about these'''
        send_thread = threading.Thread(target=self.send, daemon=True)   #create thread and put it to background
        socket_thread = threading.Thread(target=self.connection)
        send_thread.start()
        socket_thread.start()

class Main():
    @staticmethod
    def main():
        rcm = RobotConnectionManager(1201, 256)  #takes port number and buffer size as inputs for init
        rcm.start()
        
if __name__ == "__main__":
    c = Main()
    c.main()