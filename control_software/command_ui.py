#User interface(and a whacky one at that) for socket_controller module
#Oulu University of Applied Sciences
#TVT19SPL
from tkinter import *
from tkinter import scrolledtext
import RobotConnectionManager

class Main():
    def main(self):

        ip_options = [
            "192.168.100.10",
            "172.16.140.130",
            "172.16.177.128"
        ]

        port_options = [
            "29999",
            "30001",
            "30020"
        ]

        self.window = Tk()   #initialize the main ui windown
        self.window.title("Robot connection manager")    #give the window a title
        self.command_box = Entry(width=80)   #Text entry box to manually send commands
        self.output_box = scrolledtext.ScrolledText(self.window, wrap=WORD, width=80, height=30)
        self.output_box.grid(row=0, column=0, columnspan=5)
        self.command_box.grid(row=1, column=0, columnspan=5)   #place the commandbox to 0, 0 and say it takes x columnd
        self.selected_ip = StringVar()
        self.selected_port = StringVar()
        self.selected_ip.set("192.168.100.10")
        self.selected_port.set("30001")
        self.port_select = OptionMenu(self.window, self.selected_port, *port_options)
        self.ip_select = OptionMenu(self.window, self.selected_ip, *ip_options)
        self.ip_select.grid(row=2, column=2)
        self.port_select.grid(row=2, column=3)
        send_command_button = Button(text="send", command=lambda: Main.send_command_method(self)).grid(row=2, column=0) #create a button and place it to the grid
        start_rcm_button = Button(text="Start", command=self.start_rcm_method).grid(row=2, column=1)
        self.window.mainloop()   #start mainloop to display the window

    def update_output_stream(self):
        self.output_box.insert(INSERT, self.rcm.get_recv_buffer())  #Insert text from the socket, or bytes as text, not formatted at all
        self.output_box.see(END)  #scrolls the "wall of text" to the bottom so most recent entry is always visible
        self.window.after(1000, self.update_output_stream)  #after is a tkinter method that allows this function to call itself after a time peroid

    def send_command_method(self):
        command = self.command_box.get() + "\n" #get input and append newline to it for the robot to execute command as an instruction
        #self.command_box.delete(0, END) #clear command_box
        self.rcm.send(command)  #send command using rcm objects method
        
    def start_rcm_method(self):
        self.rcm = RobotConnectionManager.RobotConnectionManager(self.selected_ip.get(), int(self.selected_port.get()), 1024) #as in obj = Module.Class()
        #TODO ip address is hardcoded here. fix that
        #self.rcm.robot_address = "192.168.100.10"
        #self.rcm.robot_address = "172.16.140.130"
        #self.rcm.robot_address = "172.16.177.128"
        self.rcm.begin(mode="client")
        self.output_box.insert(INSERT, "RCM running")   #This just acts as delay so the rcm has time to start, sub optimal fix, but will do for now
        self.update_output_stream() #start a self calling function

if __name__ == "__main__":
    c = Main()
    c.main()