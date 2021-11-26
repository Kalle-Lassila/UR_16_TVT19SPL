#User interface(and a whacky one at that) for socket_controller module
#Oulu University of Applied Sciences
#TVT19SPL

from tkinter import Tk, scrolledtext, StringVar, Button, OptionMenu, Entry, WORD, INSERT, END, DISABLED, NORMAL
import RobotConnectionManager

class Main():
    def main(self):
        #options for ip dropdown menu
        ip_options = [
            "192.168.100.10",
            "172.16.140.130",
            "172.16.177.128"
        ]

        #options for port dropdown menu
        port_options = [
            "29999",
            "30001",
            "30020"
        ]
        
        #initialize the main ui window
        self.window = Tk()

        #give the window a title
        self.window.title("Robot connection manager")

        #StringVar can be used for example as a label for a button
        self.selected_ip = StringVar()
        self.selected_port = StringVar()

        #Set starting values for StringVars
        self.selected_ip.set("192.168.100.10")
        self.selected_port.set("30001")
        
        #################Create widgets#################
        self.command_box = Entry(width=80)   #Text entry box to manually send commands
        self.output_box = scrolledtext.ScrolledText(self.window, wrap=WORD, width=80, height=30)    #dimensions are in characters
        self.port_select = OptionMenu(self.window, self.selected_port, *port_options)   #OptionMenu is a dropdown menu
        self.ip_select = OptionMenu(self.window, self.selected_ip, *ip_options)
        self.send_command_button = Button(text="send",state=DISABLED, command=lambda: Main.send_command_method(self))#create a button
        start_rcm_button = Button(text="Start", command=self.start_rcm_method)

        #################Place widgets in the main window#################
        self.output_box.grid(row=0, column=0, columnspan=5)     #place the output_box to 0, 0 and say it takes x columns
        self.command_box.grid(row=1, column=0, columnspan=5)
        self.ip_select.grid(row=2, column=2)
        self.port_select.grid(row=2, column=3)
        self.send_command_button.grid(row=2, column=0)
        start_rcm_button.grid(row=2, column=1)
        
        #start mainloop to display the window
        self.window.mainloop()

    def update_output_stream(self):
        '''periodically updates the ScrolledText widget to display new information'''
        self.output_box.insert(INSERT, self.rcm.get_recv_buffer())  #Insert text from the socket, or bytes as text, not formatted at all, other than in get_recv_buffer
        self.output_box.see(END)  #scrolls the "wall of text" to the bottom so most recent entry is always visible
        self.window.after(10, self.update_output_stream)    #after() is a tkinter method that allows this function to call itself after a time peroid (in milliseconds)

    def send_command_method(self):
        '''Get contents from input Entry widget and send it out'''
        command = self.command_box.get() + "\n" #get input and append newline to it for the robot to execute command as an instruction
        #self.command_box.delete(0, END) #clear command_box
        self.output_box.insert(INSERT, f"Sent command: {command}")
        self.rcm.send(command)  #send command using rcm objects method

    def return_key_event_handler(self, event):
        self.send_command_method()
        
    def start_rcm_method(self):
        self.rcm = RobotConnectionManager.RobotConnectionManager(self.selected_ip.get(), int(self.selected_port.get()), 1) #as in obj = Module.Class()
        self.rcm.begin(mode="client")

        #enable send command button and bind to enter key
        self.send_command_button.configure(state=NORMAL)
        self.window.bind("<Return>", self.return_key_event_handler)

        self.output_box.insert(INSERT, "RCM running...\n")   #This just acts as delay so the rcm has time to start, sub optimal fix, but will do for now
        self.update_output_stream() #start a self calling function

if __name__ == "__main__":
    c = Main()
    c.main()