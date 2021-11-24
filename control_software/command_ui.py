#User interface for socket_controller module
#Oulu University of Applied Sciences
#TVT19SPL
from tkinter import *
import RobotConnectionManager

class Main():
    def main(self):
        self.window = Tk()   #initialize the main ui windown
        self.window.title("Robot connection manager")    #give the window a title
        self.command_box = Entry(width=80)   #Text entry box to manually send commands
        self.command_box.grid(row=0, column=0, columnspan=5)   #place the commandbox to 0, 0 and say it takes x columnd
        send_command_button = Button(text="send", command=lambda: Main.send_command_method(self)).grid(row=1, column=0) #create a button and place it to the grid
        start_rcm_button = Button(text="Start", command=self.start_rcm_method()).grid(row=1, column=1)
        self.window.mainloop()   #start mainloop to display the window

    def send_command_method(self):
        command = self.command_box.get() + "\n" #get input and append newline to it for the robot to execute command as an instruction
        #self.command_box.delete(0, END) #clear command_box
        print(command)  #a test print
        self.rcm.send(command)
        
    def start_rcm_method(self):
        self.rcm = RobotConnectionManager.RobotConnectionManager(30001, 4096)
        self.rcm.robot_address = "192.168.100.10"
        self.rcm.begin(mode="client")

if __name__ == "__main__":
    c = Main()
    c.main()