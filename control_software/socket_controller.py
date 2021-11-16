#socket_controller module for handling comms with ur16e and ur10 robots
#Oulu University of Applied Sciences
#TVT19SPL
#Currently robot needs to be in local control mode and the following function must be running in the robot
#interpreter_mode(clearQueueOnEnter=False)
import socket, threading, time

class RobotConnectionManager():
    '''Creates socket for communicating with the robot and handles recieved TCP messages'''
    def __init__(self, port: int, buffer: int):
        self.robot_port = port  #port used to communicate with the ur control box
        self.buffer_size = buffer   #size of the message buffer used(the number of bytes in each message sent by the robot)
        
    def server_connection(self):
        '''Starts and in the future manages socket connection to the robot or any socket for that matter'''
        #TODO unexpected disconnections are not handled at all
        self.base_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #initialize socket object
        self.base_socket.bind(("0.0.0.0", self.robot_port))    #bind the socket to unroutable address for now, and listen to robot_port
        self.base_socket.listen(5) #start listening and allow 5 failed attempts to connect
        self.robot_socket, self.robot_address = self.base_socket.accept()
        while True:
            message = self.robot_socket.recv(self.buffer_size)  #get buffer_size of bytes from socket buffer
            message = message.decode("utf-8")   #decode bytes to utf-8 character string
            print(message)

    def client_connection(self):
        self.robot_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.robot_socket.connect((self.robot_address, self.robot_port))
        while True:
            #TODO This resets user input with each print... Fix it
            time.sleep(1)
            #message = self.robot_socket.recv(self.buffer_size)
            #message = message.decode("utf-8")
            #print(message)
    
    def send(self):
        '''Take user input and sen it to socket'''
        #TODO command messages should only be sent when the robot is ready to recieve new instructions
        while True:
            message = input()   #Commands can be entered as in "popup("Hi")"
            message += "\n" #append newline to the end to avoid always typing it
            self.robot_socket.send(bytes(message,"utf-8"))  #use the socket created in rcm to send string as bytes
    
    def begin(self, mode: str):
        '''Automatically creates needed threads so user does not need to worry about these.
        possible options for mode are: "server" and "client"'''
        if mode == "client":
            connection_thread = threading.Thread(target=self.client_connection)
        elif mode == "server":
            connection_thread = threading.Thread(target=self.server_connection)

        send_thread = threading.Thread(target=self.send, daemon=True)
        send_thread.start()
        connection_thread.start()

class Main():
    @staticmethod
    def main():
        rcm = RobotConnectionManager(30020, 4096)   #takes port number and buffer size as inputs for init
        rcm.robot_address = "172.16.140.130"    #ip of the robot, needed in client mode
        rcm.begin("client")  #start rcm in client mode
        #rcm.start_server()  #start rcm in server mode
        
if __name__ == "__main__":
    c = Main()
    c.main()