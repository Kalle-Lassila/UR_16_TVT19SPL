#User interface(and a whacky one at that) for socket_controller module
#Oulu University of Applied Sciences
#TVT19SPL

from tkinter import Tk, scrolledtext, StringVar, Button, OptionMenu, Entry, WORD, INSERT, END, DISABLED, NORMAL
from tkinter.constants import NO
import RobotConnectionManager, os, time

class Main():
    def main(self):
        #TODO, make this __init__()
        self.started = False
        #options for ip dropdown menu
        ip_options = [
            "192.168.100.10",
            "172.16.140.130",
            "172.16.177.128"
        ]

        #options for port dropdown menu
        port_options = [
            "1201",
            "29999",
            "30001",
            "30002",
            "30020"
        ]

        #options for file dropdown menu
        self.update_file_options()
        if not self.file_options:
            self.file_options = ["empty"]

        #initialize the main ui window
        self.window = Tk()

        #give the window a title
        self.window.title("Robot commander")

        #StringVar can be used for example as a label for a button
        self.selected_ip = StringVar()
        self.selected_port = StringVar()
        self.selected_file = StringVar()

        #Set starting values for StringVars
        self.selected_ip.set("172.16.140.130")
        self.selected_port.set("29999")
        self.selected_file.set("empty")
        
        #################Create widgets#################
        self.command_box = Entry(width=80)   #Text entry box to manually send commands
        self.output_box = scrolledtext.ScrolledText(self.window, wrap=WORD, width=80, height=30)    #dimensions are in characters
        self.port_select = OptionMenu(self.window, self.selected_port, *port_options)   #OptionMenu is a dropdown menu
        self.ip_select = OptionMenu(self.window, self.selected_ip, *ip_options)
        self.file_select = OptionMenu(self.window, self.selected_file, *self.file_options)
        self.send_command_button = Button(text="send",state=DISABLED, command=lambda: Main.send_command_method(self))#create a button
        self.start_rcm_button = Button(text="Start", command=self.start_rcm_method)
        self.send_file_button = Button(text="Send file", state=DISABLED, command=self.send_file)

        #################Place widgets in the main window#################
        self.output_box.grid(row=0, column=0, columnspan=6)     #place the output_box to 0, 0 and say it takes x columns
        self.command_box.grid(row=1, column=0, columnspan=6)
        self.send_command_button.grid(row=2, column=0)
        self.start_rcm_button.grid(row=2, column=1)
        self.ip_select.grid(row=2, column=2)
        self.port_select.grid(row=2, column=3)
        self.send_file_button.grid(row=2, column=4)
        self.file_select.grid(row=2, column=5)
        
        #start mainloop to display the window
        self.window.mainloop()

    def update_output_stream(self):
        '''periodically updates the ScrolledText widget to display new information'''
        if self.started == True:
            self.window.after(100, self.update_output_stream)    #after() is a tkinter method that allows this function to call itself after a time peroid (in milliseconds)
            #Insert text from the socket, or bytes as text, not formatted at all, other than in get_recv_buffer
            self.output_box.insert(INSERT, self.rcm.get_recv_buffer())
            #scrolls the "wall of text" to the bottom so most recent entry is always visible
            self.output_box.see(END)

    def send_command_method(self):
        '''Get contents from input Entry widget and send it out'''
        #Only append newline if it's needed
        if self.rcm.get_port() in [30001, 30002, 30003]: command = self.command_box.get() + "\n" #get input and append newline to it for the robot to execute command as an instruction
        else: command = self.command_box.get()
        #self.command_box.delete(0, END) #clear command_box
        self.output_box.insert(INSERT, f"Sent command: {command}\n")
        self.rcm.send_str(command)  #send command using rcm objects method

    def return_key_event_handler(self, event):
        self.send_command_method()

    def send_file(self):
        if self.selected_file.get() != "empty":
            with open(f"{__file__.replace('command_ui.py', f'upload/{self.selected_file.get()}')}", "rb") as file:    #maybe concatenated formatstrings are not a good idea
                self.rcm.send_bytes(file.read(1024))

    def update_file_options(self):
        self.file_options = os.listdir(__file__.replace("command_ui.py","upload"))

    def disconnect_method(self):
        self.window.after_cancel(self.update_output_stream) #cancelling is in fashion nowdays, right?
        self.started = False    #used to track if output text should be updated
        time.sleep(0.2) #to allow update_output_stream to finish before disconnecting
        self.rcm.disconnect()

        #reconfigure buttons
        self.send_file_button.configure(state=DISABLED)
        self.send_command_button.configure(state=DISABLED)
        self.ip_select.configure(state=NORMAL)
        self.port_select.configure(state=NORMAL)
        self.start_rcm_button.configure(text="Start", command=self.start_rcm_method)    #configure start button to be a start button
        self.window.unbind("<Return>")
        
    def start_rcm_method(self):
        self.rcm = RobotConnectionManager.RobotConnectionManager(self.selected_ip.get(), int(self.selected_port.get()), 1) #as in obj = Module.Class()
        if self.selected_port in [30001, 30002, 30003]: self.rcm.begin(mode="client")
        else: self.rcm.begin(mode="server")

        self.started = True #used to track if output text should be updated

        #disable ui buttons once connected
        self.ip_select.configure(state=DISABLED)
        self.port_select.configure(state=DISABLED)

        #make start_rcm_button to be a stop button
        self.start_rcm_button.configure(text="stop", command=self.disconnect_method)

        #enable send command button and bind send to enter key
        self.send_command_button.configure(state=NORMAL)
        self.window.bind("<Return>", self.return_key_event_handler)

        #enable file sending if port is capable of receiving 
        if self.rcm.get_port() in [30001, 30002, 30003]:
            self.send_file_button.configure(state=NORMAL)

        self.output_box.insert(INSERT, "RCM running...\n")   #This just acts as delay so the rcm has time to start, sub optimal fix, but will do for now
        self.update_output_stream() #start a self calling function

if __name__ == "__main__":
    c = Main()
    c.main()