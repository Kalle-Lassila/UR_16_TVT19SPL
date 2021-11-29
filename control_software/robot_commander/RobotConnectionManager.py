#socket_controller module for handling comms with ur16e and ur10 robots
#Oulu University of Applied Sciences
#TVT19SPL
#####can be used for port 30020 operation to send URscript commands
    #Currently robot needs to be in local control mode and the following function must be running in the robot
    #interpreter_mode(clearQueueOnEnter=False)

import socket, threading, time

class RobotConnectionManager():
    '''Creates socket for communicating with the robot and handles recieved TCP messages'''
    def __init__(self, ip: str, port: int, buffer: int):
        self.robot_address = ip
        self.__robot_port = port  #port used to communicate with the ur control box
        self.buffer_size = buffer   #size of the message buffer used(the number of bytes in each message sent by the robot)
                                    #Can in theory be modified on the fly
        
    def __server_connection(self):
        '''Starts and in the future manages socket connection to the robot or any socket for that matter'''
        #TODO unexpected disconnections are not handled at all
        self.__base_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #initialize socket object
        self.__base_socket.bind(("0.0.0.0", self.__robot_port))    #bind the socket to unroutable address for now, and listen to __robot_port
        self.__base_socket.listen(5) #start listening and allow 5 failed attempts to connect
        self.__robot_socket, self.robot_address = self.__base_socket.accept()   #accept inbound connection
        # while True:
        #     message = self.__robot_socket.recv(self.buffer_size)  #get buffer_size of bytes from socket buffer
        #     message = message.decode("utf-8")   #decode bytes to utf-8 character string
        #     print(message)

    def __client_connection(self):
        '''Connect to a server socket'''
        self.__robot_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #initialize socket
        self.__robot_socket.connect((self.robot_address, self.__robot_port))    #Connect as a client to (remote address, port)
    
    def get_recv_buffer(self) -> str:
        '''Get the current buffer contents and return it'''
        #TODO this can prob get stuck in an infinite loop if data is constantly received
        #Set the socket to non-blocking
        self.__robot_socket.setblocking(False)

        #Inits
        data = []   #complete data
        part = None #partial data, used inside the loop to collect parts
        begin = time.time() #current time
        timeout = 0.01  #in seconds
        
        while True:
            #if we have data, and timeout has passed then quit
            if data and time.time()-begin > timeout:
                break
            #if not, wait a little longer, not sure if necessary: Internet told me to do this
            elif time.time()-begin > timeout*2:
                break
            #try to get data from buffer, non-blocking recv() returns immediately and raises an exeption if buffer was empty
            try:
                part = self.__robot_socket.recv(self.buffer_size)
                if part:
                    data.append(part.decode("utf-8"))
                    begin=time.time()
            except: 
                pass
        #append newline when in server mode
        if self.get_port() not in [30001, 30002, 30003] and data: data.append("\n")
        return ''.join(data)    #combine all parts into one string

    def _send_input(self):
        '''Take user input and send it to socket'''
        #TODO command messages should only be sent when the robot is ready to recieve new instructions
        while True:
            message = input("give input: ")   #Commands can be entered as in "popup("Hi")"
            message += "\n" #append newline to the end to avoid always typing it
            self.__robot_socket.send(bytes(message,"utf-8"))  #use the socket created in rcm to send string as bytes
    
    def send_str(self, message: str):
        '''take input from another module and send it'''
        self.__robot_socket.send(bytes(message,"utf-8"))  #use the socket created in rcm to send string as bytes

    def send_bytes(self, message: bytes):
        '''take input from another module and send it'''
        self.__robot_socket.send(message)

    def begin(self, mode: str):
        '''Automatically creates needed threads so user does not need to worry about these.
        possible options for mode are: "server" and "client"'''
        if mode == "client":   connection_thread = threading.Thread(target=self.__client_connection)
        elif mode == "server": connection_thread = threading.Thread(target=self.__server_connection)
        
        connection_thread.start()

    def disconnect(self):
        self.__robot_socket.close()

    def get_port(self) -> int:
        return self.__robot_port

class Main():
    @staticmethod
    def main():
        rcm = RobotConnectionManager(30001, 4096)   #takes port number and buffer size as inputs for init
        #rcm.robot_address = "192.168.100.10"    #ip of the robot, needed in client mode
        rcm.robot_address = "172.16.140.130"
        rcm.begin("client")  #start rcm in client mode
        send_thread = threading.Thread(target=rcm._send_input, daemon=True)
        send_thread.start()
        #rcm.start_server()  #start rcm in server mode
        
if __name__ == "__main__":
    c = Main()
    c.main()
