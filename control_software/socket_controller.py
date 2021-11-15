import socket, threading



class RobotConnectionManager():
    def __init__(self, port: int, buffer: int):
        self.robot_port = port  #port used to communicate with the ur control box
        #TODO logic for determining message size dynamically, must also probably be implemented on the robot side
        self.buffer_size = buffer   #size of the message buffer used(the number of bytes in each message sent by the robot)
        
    def start(self):
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

class UserInterface():
    def __init__(self, rcm: RobotConnectionManager):
        self.rcm = rcm  #rcm object is needed for it contains the socket that we can use to send data
    
    def send_data(self):
        print("ui thread started")
        message = input()
        self.rcm.robot_socket.send(bytes(message,"utf-8"))

class Main():
    @staticmethod
    def main():
        rcm = RobotConnectionManager(1201, 14)
        ui = UserInterface(rcm)
        rcm_thread = threading.Thread(rcm.start())  #create a thread so communication and user input can happen simultaneously
        rcm_thread.start()
        ui_thread = threading.Thread(ui.send_data())
        ui_thread.start()
        



if __name__ == "__main__":
    c = Main()
    c.main()